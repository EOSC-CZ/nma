import "@less/components/custom-components.less";
import $ from 'jquery';

$('.tabular.menu .item').tab();
$(function () {
  // Resolve references to vocabulary item with actual title from metadata
  $('.tabular.menu .item').each(function () {
    const $el = $(this);
    const type = $el.data('vocabulary-type');
    const id = $el.data('vocabulary-item-id');
    const extraProp = $el.data('vocabulary-extra-query-prop');
    const url = `/api/vocabularies/${type}`;

    // Skip if either required attribute is missing or empty
    if (!type || !id) {
      return;
    }

    const setLabelFromTitle = (titles) => {
      const prefs = navigator.languages || [navigator.language || 'en'];
      let label = '';

      for (const lang of prefs) {
        if (titles[lang]) {
          label = titles[lang];
          break;
        }
      }

      if (!label && titles.en) label = titles.en;
      if (!label) label = Object.values(titles)[0] || '';
      if (label) $el.text(label);
    };

    const fetchById = () => {
      return $.getJSON(`${url}/${id}`)
        .done((data) => {
          setLabelFromTitle(data.title || {});
        })
        .fail((jqXHR) => {
          if (jqXHR.status === 404 && extraProp) {
            if (extraProp) {
              fetchByQuery();
            }
          }
        });
    };

    const fetchByQuery = () => {
      const query = encodeURIComponent(`props.${extraProp}:${id}`);
      $.getJSON(`${url}?q=${query}`)
        .done((data) => {
          const hit = data?.hits?.hits?.[0];
          if (hit && hit.title) {
            setLabelFromTitle(hit.title);
          }
        });
    };

    fetchById();
  });
});