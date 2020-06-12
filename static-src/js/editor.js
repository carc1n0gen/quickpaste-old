/**
 * Rich code editor for Quickpaste
 *
 * Constructor takes as input an HTMLForm element that contains the following elements:
 *   - Textarea
 *   - Contenteditable element
 *   - Select element with class "indent" for indentation style
 *   - Select element named "extension" for language selection
 *   - Element with class "lines" for containing line numbering
 */

class RichEditor {
    constructor(form) {
        this.form = form;
        this.editor = this.form.querySelector('[contenteditable]');
        this.highlightTimer;
        this.indentControl = this.form.querySelector('.indent');
        this.lines = this.form.querySelector('.lines');
        this.textarea = this.form.text;


        /*
         * Initialization
         */
        this.editor.classList.remove('rich-disabled');
        this.form.querySelector('.indent-control').classList.remove('rich-disabled');
        this.textarea.classList.add('rich-disabled');
        this.editor.innerHTML = this.editor.innerText; // Turn contents of div from plain text to HTML
        this.lineNumbers(); // Initialize line numbers based on initial contents
        this.detectIndentation(); // Set the indent control and editor to correct indentation
        this.adjustCaret = 0; // In some situations we need to adjust +/- where the caret should end up


        /*
         * Bind various events
         */

        // Only submit if not empty
        this.form.addEventListener('submit', e => {
            e.preventDefault();
            if (this.textarea.value && this.textarea.value.trim()) {
                this.textarea.value = this.textarea.value.trim();
                form && form.submit();
            }
        });

        // Trigger a highlight request if selected language changes
        this.form.extension.addEventListener('change', this.highlight.bind(this));

        this.editor.addEventListener('keydown', e => {
            this.lineNumbers();
            this.textarea.value = this.editor.innerText;

            // Check if keypress was just navigating rather than mutating contents
            const noInsert = [
                "AltLeft", "AltRight", "ArrowDown", "ArrowRight", "ArrowLeft", 
                "ArrowUp", "CapsLock", "ControlLeft", "ControlRight", "End", 
                "Enter", "Escape", "Home", "OSLeft", "OSRight", "PageDown", 
                "PageUp", "ShiftLeft", "ShiftRight", "Tab"
            ];
            if(!noInsert.includes(e.key)) {
                // Only send the request if the user has stopped typing for 1 second.
                window.clearTimeout(this.highlightTimer);
                this.highlightTimer = window.setTimeout(this.highlight.bind(this), 1000);
            }

            if(e.key == "Tab") {
                e.preventDefault();
                this.insertIndent();
            }

            if(e.key == "Enter" && this.editor.querySelector('.highlight')) {
                e.preventDefault();
                this.insertNewLine();
            }
        });

        this.editor.addEventListener('paste', e => {
            // Timer is necessary because we need the paste event to finish and 
            // update the value of the editor
            window.setTimeout(() => {
                // Required for insertNewLine() to work properly
                this.editor.innerHTML = this.editor.innerText;
                this.textarea.value = this.editor.innerText;
            }, 100);
            window.setTimeout(this.detectIndentation.bind(this), 100);
            window.setTimeout(this.lineNumbers.bind(this), 100);
        });

        // Autoformat code when indentation style changes
        this.indentControl.addEventListener('change', e => {
            let old_size = this.indentation.size;
            let type, size;
            [type, size] = this.indentControl.value.split('-');

            if(type == 'spaces') {
                // Replace old blocks of spaces with new blocks
                this.editor.innerText = this.editor.innerText.replace(/^ +/gm, function(match) {
                    return ' '.repeat(match.length/old_size*size);
                });
                // Replace tabs with spaces
                this.editor.innerText = this.editor.innerText.replace(/^\t+/gm, function(match) {
                    return ' '.repeat(match.length*size);
                });
            } else {
                // Replace spaces with tabs
                this.editor.innerText = this.editor.innerText.replace(/^ +/gm, function(match) {
                    return "\t".repeat(match.length/old_size);
                });

                // Set tab width
                this.editor.style.tabSize = size;
                this.editor.style.MozTabSize = size;
            }

            this.indentation = {
                'size': size,
                'type': type
            }

            // Update textarea and rehighlight
            this.textarea.value = this.editor.innerText;
            this.highlight();
        });
    }


    get lang() {
        return this.form.extension.value || 'txt';
    }


    detectIndentation() {
        this.indentation = {
            'size': 2,
            'type': 'spaces'
        };

        const matches = this.editor.innerText.match(/^[ \t]+/gm);
        if(matches) {
            if(matches[0].match(/^\t/gm)) {
                this.indentation.type = 'tabs';
            } else if([2, 4, 8].includes(matches[0].length)) {
                this.indentation.size = matches[0].length;
            } else {
                console.log("Could not detect indenting. Defaulting to 2 spaces.");
            }
            this.indentControl.value = this.indentation.type + '-' + this.indentation.size;
            return this.indentation;
        }
        return false;
    }

    // Dispatch a request to app for syntax highlighting
    async highlightRequest() {
        const data = new FormData();
        data.append('text', this.editor.innerText);
        data.append('lang', this.lang);
        const response = await fetch('/highlight', {
            method: 'POST',
            mode: 'same-origin',
            cache: 'no-cache',
            credentials: 'same-origin',
            body: data
          });
        return response.text();
    }

    // Wrapper to deal with async syntax highlight request and consequences
    highlight() {
        /*
         * Don't bother highlighting if the editor is empty.
         * Similarly, Pygments' auto-detection feature sucks for our snippets it seems?
         * So highlighting might be too problematic.
         */
        if(this.editor.innerText.trim() != '') {
            console.log("Caret adjust:" + this.adjustCaret);
            this.highlightRequest().then(data => {
                // Save cursor position and restore it after replacing editor's innerHTML
                const restoreCaret = this.saveCaretPosition();
                this.editor.innerHTML = data;
                restoreCaret(this.adjustCaret);
                this.adjustCaret = 0;
            });
        }
    }

    insert(node) {
        const selection = window.getSelection();
        const range = selection.getRangeAt(0);
        range.insertNode(node);
        range.setStartAfter(node);
        range.collapse(true);
        selection.removeAllRanges();
        selection.addRange(range);
    }

    insertIndent(level = 1) {
        const contents = (this.indentation.type == "tabs") 
            ? "\t".repeat(level) 
            : " ".repeat(this.indentation.size * level);
        const node = document.createTextNode(contents);

        this.insert(node);
    }

    insertNewLine() {
        const restoreCaret = this.saveCaretPosition();
        const selection = window.getSelection();
        const range = selection.getRangeAt(0);
        range.setStart(this.editor, 0);
        const lines = range.toString().split(/\r\n|\r|\n/);
        range.collapse(true);
        selection.removeAllRanges();
        selection.addRange(range);
        let indentLevel = 0;
        if(lines) {
            const indentation = lines[lines.length - 1].match(/^[ \t]+/gm);

            if(indentation) {
                indentLevel = (this.indentation.type == "tabs") 
                    ? indentation[0].length 
                    : indentation[0].length / this.indentation.size;
            }
        }

        restoreCaret();
        this.insert(document.createElement("br"));
        this.insertIndent(indentLevel);
        this.lineNumbers();
        this.adjustCaret = 1;
    }

    // Renumbers the lines down the side of the code editor
    lineNumbers() {
        const val = this.editor.innerText;
        const num_lines = val.trim().split(/\r\n|\r|\n/).length;
        this.lines.innerHTML = null;
        for(let i = 1; i <= num_lines; i++) {
            const l = document.createElement('div');
            l.classList.add('line');
            l.innerText = i;
            this.lines.appendChild(l);
        }
    }

    /*
     * saveCaretPosition() and getTextNodePosition() help save and restore the 
     * position of the caret in the contenteditable element after its innerHTML is 
     * replaced.
     *
     * Code modified from example on StackOverflow
     */
    saveCaretPosition() {
        const self = this;
        const selection = window.getSelection();
        const range = selection.getRangeAt(0);
        range.setStart(self.editor, 0);
        const len = range.toString().length;

        return function restore(adjust=0) {
            if(adjust > len) {
                adjust = 0;
            }
            const pos = self.getTextNodeAtPosition(self.editor, len + adjust);
            selection.removeAllRanges();
            const range = new Range();
            range.setStart(pos.node, pos.position);
            selection.addRange(range);
        }
    }

    getTextNodeAtPosition(root, index) {
        let lastNode = null;

        let treeWalker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT, function next(elem) {
            if(index >= elem.textContent.length){
                index -= elem.textContent.length;
                lastNode = elem;
                return NodeFilter.FILTER_REJECT
            }
            return NodeFilter.FILTER_ACCEPT;
        });
        const c = treeWalker.nextNode();
        return {
            node: c ? c : root,
            position: c ? index :  0
        };
    }
}