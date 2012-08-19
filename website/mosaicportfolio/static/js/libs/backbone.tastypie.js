//    Copyright (c) 2012 Andrew McCloud
//
//    https://github.com/amccloud/backbone-tastypie
//
//        Permission is hereby granted, free of charge, to any person
//    obtaining a copy of this software and associated documentation
//    files (the "Software"), to deal in the Software without
//    restriction, including without limitation the rights to use,
//        copy, modify, merge, publish, distribute, sublicense, and/or sell
//    copies of the Software, and to permit persons to whom the
//    Software is furnished to do so, subject to the following
//    conditions:
//
//        The above copyright notice and this permission notice shall be
//    included in all copies or substantial portions of the Software.
//
//        THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
//        EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
//    OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
//    NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
//    HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
//        WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
//    FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
//    OTHER DEALINGS IN THE SOFTWARE.

(function($, _, Backbone) {
    Backbone.Tastypie = {
        defaultLimit: 20
    };

    _.extend(Backbone.Model.prototype, {
        idAttribute: 'resource_uri',

        url: function() {
            var uri = this.get('resource_uri');

            if (uri !== undefined) {
                return uri;
            }

            var url = getValue(this, 'urlRoot') || getValue(this.collection, 'urlRoot') || urlError();

            if (this.get('id') !== undefined)
                return url + this.get('id') + '/';

            return url;

        },
        _getId: function() {
            if (this.has('id'))
                return this.get('id');

            return _.chain(this.get('resource_uri').split('/')).compact().last().value();
        }
    });

    _.extend(Backbone.Collection.prototype, {
        initialize: function(collections, options) {
            _.bindAll(this, 'fetchNext', 'fetchPrevious');

            this.meta = {};
            this.filters = {
                limit: Backbone.Tastypie.defaultLimit,
                offset: 0
            };

            if (options && options.filters)
                _.extend(this.filters, options.filters);
        },
        url: function(models) {
            var url = this.urlRoot;

            if (models) {
                var ids = _.map(models, function(model) {
                    return model._getId();
                });

                url += 'set/' + ids.join(';') + '/';
            }

            return url + this._getQueryString();
        },
        parse: function(response) {
            if (response && response.meta)
                this.meta = response.meta;

            return response && response.objects;
        },
        fetchNext: function(options) {
            options = options || {};
            options.add = true;

            this.filters.limit = this.meta.limit;
            this.filters.offset = this.meta.offset + this.meta.limit;

            if (this.filters.offset > this.meta.total_count)
                this.filters.offset = this.meta.total_count;

            return this.fetch.call(this, options);
        },
        fetchPrevious: function(options) {
            options = options || {};
            options.add = true;
            options.at = 0;

            this.filters.limit = this.meta.limit;
            this.filters.offset = this.meta.offset - this.meta.limit;

            if (this.filters.offset < 0){
                this.filters.limit += this.filters.offset;
                this.filters.offset = 0;
            }

            return this.fetch.call(this, options);
        },
        _getQueryString: function() {
            if (!this.filters)
                return '';

            return '?' + $.param(this.filters);
        }
    });

    // Helper function from Backbone to get a value from a Backbone
    // object as a property or as a function.
    var getValue = function(object, prop) {
        if ((object && object[prop]))
            return _.isFunction(object[prop]) ? object[prop]() : object[prop];
    };

    // Helper function from Backbone that raises error when a model's
    // url cannot be determined.
    var urlError = function() {
        throw new Error('A "url" property or function must be specified');
    };
})(window.$, window._, window.Backbone);