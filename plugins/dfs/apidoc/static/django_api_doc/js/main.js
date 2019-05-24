/**
 * Created by leaves on 16/9/27.
 */
var base_url = window.location.pathname;

Vue.config.delimiters = ["{[", "]}"];

new Vue({
    el: '#app',
    data: {
        url_names: [],
        url_namespaces: [],
        doc_title: 'Welcome to Django API Document'
    },
    ready: function () {
        var url = base_url + 'menu/';
        this.$http.get(url).then(function (response) {
            this.url_namespaces = response.data.url_namespaces;
            this.url_names = response.data.url_names;
            this.doc_title = response.data.doc_title;
            document.title = response.data.doc_title
        }, function (response) {
            alert('Error');
        })
    },
    methods: {
        treeViewShow: function (e) {
            console.log(e);
            e.target.parentElement.classList.toggle('active');
            // e.parents('.treeview').addClass('active');
            // e.parents('.treeview').find('.treeview-menu').addClass('menu-open');
        }
    }
});

var DocContent = Vue.extend({
    template: '#doc-content',
    data: function() {
        return {
            doc: this.doc
        };
    },
    ready: function () {
        var url = base_url + this.$route.params.url_name + '/';
        this.$http.get(url).then(function (response) {
            this.doc = response.data;
        }, function (response) {
            this.doc = {
                title: 'Error'
            };
        })
    },
    filters: {
        marked: marked
    },
    route: {

    }
});


// router
var app = {};
var router = new VueRouter();
router.map({
    '/:url_name': {
        component: DocContent
    }
});
router.start(app, '#app');
