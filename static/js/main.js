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

    onkeydown = onkeyup = function (e) {
        keyState[e.key] = e.type == 'keydown';

        if (keyState['Control'] && keyState['s']) savePaste();
        if (keyState['Control'] && keyState['n']) newPaste();
        if (keyState['Control'] && keyState['i']) aboutPaste();
    }
});