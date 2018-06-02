---
---
showdown.extension('myExt', function() {
    var matches = [];
    return [
        {
            type: 'lang',
            regex: /\(#([^]+?)\)/gi,
            replace: function(s, match) {
                matches.push(match);
                var n = matches.length - 1;
                return '(' + url + '#%PLACEHOLDER' + n + '%)';
            }
        },
        {
            type: 'output',
            filter: function (text) {
                for (var i=0; i< matches.length; ++i) {
                    var pat = '%PLACEHOLDER' + i + '% *';
                    text = text.replace(new RegExp(pat, 'gi'), matches[i]);
                }
                //reset array
                matches = [];
                return text;
            }
        }
    ]
});

var converter = new showdown.Converter({extensions: ['myExt']});

const search = instantsearch({
  appId: '{{ site.algolia.application_id }}',
  apiKey: '{{ site.algolia.search_only_api_key }}',
  indexName: 'py-search-awesome',
  urlSync: true,
  searchFunction: function(helper) {
    var searchResults = document.getElementById('search-hits');
    if (helper.state.query === '') {
      searchResults.display='none';
      return;
    }
    helper.search();
    searchResults.display='';
  }
});

var url;

const hitTemplate = function(hit) {
  let link = `${hit.link}`;
  let header = converter.makeHtml(`${hit.header}`);
  let con = converter.makeHtml(`${hit.content}`);
  url = link;
  return `
    <div class="post-item">
      <a class="post-link" href="${link}">${header} ${link}</a>
      <p>${con}</p>
    </div>
  `;
}


search.addWidget(
  instantsearch.widgets.searchBox({
    container: '#search-searchbar',
    placeholder: 'Search Awesome Lists...',
    poweredBy: true
  })
);

search.addWidget(
  instantsearch.widgets.hits({
    container: '#search-hits',
    templates: {
      empty: 'No results',
      item: hitTemplate
    }
  })
);

search.start();
