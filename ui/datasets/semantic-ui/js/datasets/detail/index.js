/* "show more text" functionality with CSS trick: https://paulbakaus.com/multiline-truncated-text-with-show-more-button-with-just-css/ */
const observer = new ResizeObserver(entries => {
  for (let entry of entries) {
    entry.target.classList[entry.target.scrollHeight > entry.contentRect.height ? 'add' : 'remove']('dom-truncated');
  }
});

let index = 1;
while (true) {
  const checkboxElem = document.getElementById("detail-description-expanded-" + index);
  const descriptionElem = document.getElementById("detail-description-" + index);
  if (!descriptionElem || !checkboxElem) break;

  checkboxElem.checked = false;

  observer.observe(descriptionElem);
  
  index++;
}