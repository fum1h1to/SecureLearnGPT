// このアプリで扱うページのIDを配列に格納
const pages = [
  {
    id: 'top',
    url: '/'
  }, {
    id: 'problem',
    url: '/problem'
  }, {
    id: 'answer',
    url: '/answer'
  }, {
    id: 'problemError',
    url: '/problemError'
  }, {
    id: 'answerError',
    url: '/answerError'
  }
];

/**
 * ページの見た目を切り替える処理
 * @param {string} pageId
 * @returns
 */
const pageViewChanger = (pageId) => {
  const basePageContainer = document.querySelectorAll('.js-basePageContainer');
  let isFound = false;

  pages.forEach((page) => {
    if (page.id === pageId) {
      isFound = true;
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

// ブラウザの戻るボタンを押された時の処理
window.addEventListener("popstate", () => {
  pages.forEach((page) => {
    if (page.url === window.location.pathname) {
      pageChanger(page.id);
    }
  });
});

// js-toTopBtnクラスを持つ要素がクリックされたときの処理、topページに遷移する
const toTopPageBtn = document.querySelectorAll('.js-toTopBtn');
toTopPageBtn.forEach((btn) => {
  btn.addEventListener('click', () => {
    pageChanger('top');
  });
});


/* ----------------------------
topページの処理
----------------------------- */
class TopPage {
  pageId = "#top";

  constructor() {
    
  }

  toTopPage = () => {
    pageViewChanger('top');
  }
}


/* ----------------------------
problemページの処理
----------------------------- */
class ProblemPage {
  pageId = "#problem";
  cenarioTyped = null;
  scenario = null;
  questions = null;
  questionEles = null;

  constructor() {
    this.questionEles = document.querySelectorAll(this.pageId + ' .js-problem-question');

    this.#initTextCounter();
    
    const answerBtn = document.querySelector(this.pageId + ' .js-problem-answer');
    answerBtn.addEventListener('click', () => {
      this.toProblemPage();
    });

    this.#init();
  }

  #init = () => {
    document.querySelector(this.pageId + ' .js-problem-progress').classList.add('is-active');

    if (this.cenarioTyped) {
      this.cenarioTyped.destroy();
    }

    document.querySelector(this.pageId + ' .js-problem-questionBox').classList.remove('is-active');
    document.querySelector(this.pageId + ' .js-problem-controlArea').classList.remove('is-active');

    this.questionEles.forEach((ele) => {
      const answerTxt = ele.querySelector('.js-problem-answerTxt');
      const answerTxtCounter = ele.querySelector('.js-problem-answerTxtCounter');
      answerTxt.value = "";
      answerTxtCounter.textContent = answerTxt.value.length;

      const questionTxt = ele.querySelector('.js-problem-questionTxt');
      questionTxt.textContent = '問題取得中...';
    });

  
    // this.#getProblemData();
  }

  toProblemPage = () => {
    this.#init();
    pageViewChanger('problem');
    
    this.#getProblemData();  
  }

  #getProblemData() {
    const sendOption = {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json; charset=utf-8',
      }
    };

    fetch('/api/problem', sendOption)
      .then(res => {
        document.querySelector(this.pageId + ' .js-problem-progress').classList.remove('is-active');
    
        return res.json();
      })
      .then((res) => {
        if (res.status == 0) {
          this.scenario = res.scenario;
          this.questions = res.questions;
          this.#setProblemData();
        } else {
          console.log("失敗");
          problemErrorPage.toProblemErrorPage(res.message);
        }
      })
      .catch(error => {
        console.log(error);
      });
  }

  #setProblemData() {
    const problemScenario = document.querySelector(this.pageId + ' .js-problem-scenarioTxt');

    this.cenarioTyped = new Typed(problemScenario, {
      strings: [this.scenario],
      typeSpeed: 25,
      showCursor: false,
      loop: false,
      onComplete: () => {
        this.questionEles.forEach((ele, index) => {
          const questionTxt = ele.querySelector('.js-problem-questionTxt');
          questionTxt.textContent = this.questions[index].question_txt;
        });

        document.querySelector(this.pageId + ' .js-problem-questionBox').classList.add('is-active');
        document.querySelector(this.pageId + ' .js-problem-controlArea').classList.add('is-active');
      }
    });
    
  }

  #initTextCounter() {
    this.questionEles.forEach((ele) => {
      const answerTxt = ele.querySelector('.js-problem-answerTxt');
      const answerTxtCounter = ele.querySelector('.js-problem-answerTxtCounter');
      answerTxtCounter.textContent = answerTxt.value.length;

      answerTxt.addEventListener('keyup', () => {
        answerTxtCounter.textContent = answerTxt.value.length;
      });
    });
  }
}

/* ----------------------------
answerページの処理
----------------------------- */
class AnswerPage {
  
}

/* ----------------------------
problemErrorページの処理
----------------------------- */
class ProblemErrorPage {
  pageId = "#problemError";

  constructor() {
    const againBtn = document.querySelector(this.pageId + ' .js-problemError-again');
    againBtn.addEventListener('click', () => {
      pageChanger('problem')
    });
  }

  toProblemErrorPage = (message) => {
    document.querySelector(this.pageId + ' .js-problemError-alert').textContent = message;
    pageViewChanger('problemError');
  }
}

/* ----------------------------
answerErrorページの処理
----------------------------- */
class AnswerErrorPage {
  
}


/* ----------------------------
全体的な処理
----------------------------- */
const topPage = new TopPage();
const problemPage = new ProblemPage();
const answerPage = new AnswerPage();
const problemErrorPage = new ProblemErrorPage();
const answerErrorPage = new AnswerErrorPage();

/**
 * pageを切り替えるための関数
 * @param {string} pageId 
 * @returns 
 */
const pageChanger = (pageId) => {

  switch (pageId) {
    case 'top':
      topPage.toTopPage();
      break;
    case 'problem':
      problemPage.toProblemPage();
      break;
    case 'answer':
      answerPage.toAnswerPage();
      break
    case 'problemError':
      problemPage.toProblemPage();
      break
    case 'answerError':
      answerPage.toAnswerPage();
      break
    default:
      console.error(pageId + 'というページは存在しません。');
      break;

  }
}