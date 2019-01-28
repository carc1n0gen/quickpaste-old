window.addEventListener('load', function () {
    var keyState = {};
    var text = document.getElementById('text');
    var form = document.getElementById('form');

    function savePaste(e) {
        e && e.preventDefault();
        if (text.value && text.value.trim()) {
            form && form.submit();
        }
    }
    form && (form.onsubmit = savePaste);

    function newPaste() {
        open('/', '_self');
    }

    function aboutPaste() {
        location.pathname !== '/about' && open('/about', '_self');
    }

    // function indentText() {

    // }

    // function unindentText() {

    // }

    onkeydown = onkeyup = function (e) {
        keyState[e.key] = e.type == 'keydown';

        // if (e.target === text && keyState['Tab']) {
        //     e.preventDefault();
        //     indentText();
        // }
        // if (e.target === text && keyState['Shift'] && keyState['Tab']) {
        //     e.preventDefault();
        //     unindentText();
        // }

        if (keyState['Control'] && keyState['s']) savePaste();
        if (keyState['Control'] && keyState['n']) newPaste();
        if (keyState['Control'] && keyState['i']) aboutPaste();
    };

    // if (text) {
    //     text.onkeydown = function (e) {
    //         if (e.key === 'Tab') {
    //             e.preventDefault();
    //         }
    //     };
    // }
});
