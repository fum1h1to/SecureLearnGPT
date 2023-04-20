// このアプリで扱うページのIDを配列に格納
const pages = [
  {
    id: 'top',
    url: '/',
  }, {
    id: 'problem',
    url: '/problem',
  }, {
    id: 'answer',
    url: '/answer',
  }, {
    id: 'problemError',
    url: '/problemError',
  }, {
    id: 'answerError',
    url: '/answerError',
  }
];

// 現在フォーカスされているページのID
let nowPageId = 'top';

/**
 * pageを切り替えるための関数
 * @param {string} pageId 
 * @returns 
 */
const pageChanger = (pageId) => {
  const basePageContainer = document.querySelectorAll('.js-basePageContainer');
  let isFound = false;

  pages.forEach((page) => {
    if (page.id === pageId) {

      isFound = true;
      nowPageId = pageId;
      window.history.pushState(null, null, page.url);

      basePageContainer.forEach((ele) => {

        ele.classList.remove('is-active');
        if (ele.id === pageId) {
          ele.classList.add('is-active');
        }
      });
    }
  });

  if (!isFound) {
    console.error(pageId + 'というページは存在しません。');
  }
}

window.addEventListener("popstate", () => {
  pages.forEach((page) => {
    if (page.url === window.location.pathname) {
      pageChanger(page.id);
    }
  });
});