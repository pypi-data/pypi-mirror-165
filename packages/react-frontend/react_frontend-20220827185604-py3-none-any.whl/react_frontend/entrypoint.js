
try {
    new Function("import('/reactfiles/frontend/main.b0722d41.js')")();
} catch (err) {
    var el = document.createElement('script');
    el.src = '/reactfiles/frontend/main.b0722d41.js';
    el.type = 'module';
    document.body.appendChild(el);
}
