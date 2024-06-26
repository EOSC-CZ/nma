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
            animation: 'fade',
            duration: '1s',
            onComplete: function () {
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
            animation: 'fade',
            duration: '1s',
            onComplete: function () {
              $element.transition('restore conditions');
              element.classList.remove('exclamation', 'triangle');
              element.classList.add('outline', 'copy');
            }
          });
      });
  }
}

function configureCopyButtons(copyButtons) {
  copyButtons.each((index, element) => {
    const text = element.dataset?.clipboardText ?? '';
    $(element).on('click', () => {
      copyToClipboard(element, text);
    });
  });
}

export function deinitializeCopyButtons(copyButtons) {
  copyButtons = copyButtons?.jquery ? copyButtons : $(copyButtons);
  copyButtons.each((index, element) => {
    const $element = $(element);
    $element.off('click');
  });
}

export function initCopyButtons(copyButtons) {
  copyButtons = copyButtons?.jquery ? copyButtons : $(copyButtons);
  // Firefox 1.0+
  const isFirefox = typeof InstallTrigger !== 'undefined';
  if (!isFirefox) {
    navigator.permissions.query({ name: "clipboard-write" })
      .then((result) => {
        if (result.state == "granted" || result.state == "prompt") {
          configureCopyButtons(copyButtons);
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
    configureCopyButtons(copyButtons);
  }
}

// Initialize clipboard copy buttons
const copyButtons = $('.copy-button');
initCopyButtons(copyButtons);


// Semantic UI accordion initialization
$('.ui.accordion')
  .accordion()
  ;
