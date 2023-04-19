// このアプリで扱うページのIDを配列に格納
const pages = [
  'top',
  'problem',
  'answer',
  'problemError',
  'answerError'
]

// 現在フォーカスされているページのID
let nowPageId = 'top';

/**
 * pageを切り替えるための関数
 * @param {string} pageId 
 * @returns 
 */
const pageChanger = (pageId) => {
  const basePageContainer = document.querySelectorAll('.js-basePageContainer');

  if (!pages.includes(pageId)) {
    console.error(pageId + 'というページは存在しません。');
    return;
  }
  nowPageId = pageId;
  basePageContainer.forEach((ele) => {
    ele.classList.remove('is-active');
    if (ele.id === pageId) {
      ele.classList.add('is-active');
    }
  });
}