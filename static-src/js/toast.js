(function() {
    window.addEventListener('load', function () {
        document.querySelectorAll('.alert-autohide').forEach((el) => {
            setTimeout(() => {
                el.classList.add('fade-out-start');
            }, 5000);
            setTimeout(() => {
                el.remove();
            }, 7000);
        });

        document.querySelectorAll('.fade-in').forEach((el) => {
            el.classList.add('fade-in-start');
        });

        document.querySelectorAll('.alert-close').forEach((el) => {
            el.addEventListener('click', (event) => {
                const target = document.querySelector(el.dataset.target);
                if (target) {
                    target.classList.add('fade-out-start');
                    setTimeout(() => {
                        target.remove();
                    }, 2000);
                }
            });
        });
    });
})();
