import $ from 'jquery';

function copyToClipboard(element, text) {
  const $element = $(element);
  if (!$element.transition('is animating')) {
    $element.transition('save conditions', { silent: true });
    element.classList.remove('outline', 'copy');
    element.classList.add('notched', 'circle', 'loading');
    navigator.clipboard.writeText(text)
      .then(() => {
        element.classList.remove('notched', 'circle', 'loading');
        element.classList.add('check');
        $element
          .transition({
            animation  : 'fade',
            duration   : '1s',
            onComplete : function() {
              $element.transition('restore conditions');
              element.classList.remove('check');
              element.classList.add('outline', 'copy');
            }
          });
      })
      .catch((err) => {
        element.classList.remove('notched', 'circle', 'loading');
        element.classList.add('exclamation', 'triangle');
        $element
          .transition({
            animation  : 'fade',
            duration   : '1s',
            onComplete : function() {
              $element.transition('restore conditions');
              element.classList.remove('exclamation', 'triangle');
              element.classList.add('outline', 'copy');
            }
          });
      });
  }
};

const copyButtons = $('.copy-button');

const configureCopyButtons = () => {
  copyButtons.each((index, element) => {
    const text = $(element).data('clipboard-text');
    $(element).on('click', () => {
      copyToClipboard(element, text);
    });
  });
};

// Firefox 1.0+
var isFirefox = typeof InstallTrigger !== 'undefined';
if (!isFirefox) {
  navigator.permissions.query({ name: "clipboard-write" })
    .then((result) => {
      if (result.state == "granted" || result.state == "prompt") {
        configureCopyButtons();
      } else {
        copyButtons.each((index, element) => {
          $(element).addClass('disabled');
        });
      }
    })
    .catch((err) => {
      copyButtons.each((index, element) => {
        $(element).remove(); // Remove the button
      });
    });
} else {
  // Firefox does not support "clipboard-write" permission
  configureCopyButtons();
}

$('.ui.accordion')
  .accordion()
;