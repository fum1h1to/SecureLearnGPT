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
      // window.history.pushState(null, null, page.url);

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
// window.addEventListener("popstate", () => {
//   pages.forEach((page) => {
//     if (page.url === window.location.pathname) {
//       pageChanger(page.id);
//     }
//   });
// });

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

  toTopPage() {
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

  // アプリ読み込み時に行う処理
  constructor() {
    this.questionEles = document.querySelectorAll(this.pageId + ' .js-problem-question');

    this.#initTextCounter();
    
    const answerBtn = document.querySelector(this.pageId + ' .js-problem-answer');
    answerBtn.addEventListener('click', async () => {
      if(this.#checkValidation()) {
        this.#disableErrorDialog();

        answerBtn.classList.add('is-loading');

        const ret = await this.#getAnswerData();
        if (ret) {
          const questionsArray = []
          this.questions.forEach((question) => {
            questionsArray.push(question.question_txt);
          });

          const message = {
            scenario: this.scenario,
            questions: questionsArray,
            commentarys: ret,
          }
          pageChanger('answer', message);
        }
        
        answerBtn.classList.remove('is-loading');
      }
    });

    this.#init();
  }

  // このページに遷移してきた時に行いたい処理
  #init() {
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

    document.querySelector(this.pageId + ' .js-problem-answer').classList.remove('is-loading');

    this.#disableErrorDialog();
  }

  // このページに遷移する処理
  toProblemPage = () => {
    window.scrollTo({top: 0});
    this.#init();
    pageViewChanger('problem');
    
    this.#getProblemData();  
  }

  // 入力値のバリデーションチェック
  #checkValidation() {
    for(let i = 0; i < 4; i++) {
      const questionTxt = document.getElementById('question' + (i + 1));
      if (questionTxt.value === "") {
        this.#showErrorDialog('入力されていない項目があります。');
        return false;
      }
      if (questionTxt.value.length > 100) {
        this.#showErrorDialog('100文字以内で入力してください。');
        return false;
      }
    }
    return true;
  }

  // 問題データを取得する処理
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
          pageChanger('problemError', res.message);
        }
      })
      .catch(error => {
        console.log(error);
      });
  }

  // 問題データを画面に表示する処理
  #setProblemData() {
    const problemScenario = document.querySelector(this.pageId + ' .js-problem-scenarioTxt');

    this.cenarioTyped = new Typed(problemScenario, {
      strings: [this.scenario],
      typeSpeed: 50,
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

  // 回答を送信する処理
  async #getAnswerData() {
    const answers_json = [];
    const answerTxts = document.querySelectorAll(this.pageId + ' .js-problem-answerTxt');
    answerTxts.forEach((answerTxt, index) => {
      answers_json.push({
        question_num: index + 1,
        answer_txt: answerTxt.value,
      });
    });

    const sendOption = {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json; charset=utf-8',
      },
      body: JSON.stringify({
        scenario: this.scenario,
        questions: this.questions,
        answers: answers_json
      })
    };

    let result = null;

    await fetch('/api/answer', sendOption)
      .then(res => { 
        return res.json();
      })
      .then((res) => {
        // console.log(res);
        if (res.status == 0) {
          const retCom = []
          res.commentarys.forEach((commentary) => {
            retCom.push(commentary.commentary_txt);
          });
          result = retCom;
        } else {
          console.log("失敗");
          this.#showErrorDialog(res.message);
        }
      })
      .catch(error => {
        console.log(error);
        this.#showErrorDialog('エラーが発生しました。再度解答を送信してみてください。');
      });

    return result;
  }

  // 入力欄の文字数カウンターの初期化
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

  // エラーダイアログを表示する処理
  #showErrorDialog(message) {
    const alertMessage = document.querySelector(this.pageId + ' .js-problem-alert');
    alertMessage.classList.add('is-active');
    alertMessage.textContent = message;
  }

  // エラーダイアログを非表示にする処理
  #disableErrorDialog() {
    const alertMessage = document.querySelector(this.pageId + ' .js-problem-alert');
    alertMessage.classList.remove('is-active');
    alertMessage.textContent = "";
  }
}

/* ----------------------------
answerページの処理
----------------------------- */
class AnswerPage {
  pageId = "#answer";

  // アプリ読み込み時の処理
  constructor() {
    const againBtn = document.querySelector(this.pageId + ' .js-answer-again');
    againBtn.addEventListener('click', () => {
      pageChanger('problem')
    });

    this.#init();
  }

  // このページの初期化処理
  #init() {
    const questionBox = document.querySelector(this.pageId + ' .js-answer-questionBox');
    questionBox.classList.remove('is-active');

    const questionEles = document.querySelectorAll(this.pageId + ' .js-problem-question');
    questionEles.forEach((ele) => {
      const questionTxt = ele.querySelector('.js-problem-questionTxt');
      questionTxt.textContent = '解説取得中...';

      const answerTxt = ele.querySelector('.js-problem-answerTxt');
      answerTxt.textContent = '';
    });

    
  }

  toAnswerPage = (message) => {
    this.#init();
    this.#setAnswerData(message.scenario, message.questions, message.commentarys)
    
    window.scrollTo({top: 0});
    pageViewChanger('answer');


    setTimeout(() => {
      const questionBox = document.querySelector(this.pageId + ' .js-answer-questionBox');
      questionBox.classList.add('is-active');
    }, 500);
  }

  #setAnswerData(scenario, questions, commentarys) {
    const problemScenario = document.querySelector(this.pageId + ' .js-answer-scenarioTxt');
    problemScenario.textContent = scenario;

    const questionTxts = document.querySelectorAll(this.pageId + ' .js-answer-questionTxt');
    questionTxts.forEach((ele, index) => {
      ele.textContent = questions[index];
    });

    const commentaryTxts = document.querySelectorAll(this.pageId + ' .js-answer-commentaryTxt');
    commentaryTxts.forEach((ele, index) => {
      ele.textContent = commentarys[index];
    });

  }
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

  toProblemErrorPage(message) {
    document.querySelector(this.pageId + ' .js-problemError-alert').textContent = message;
    pageViewChanger('problemError');
  }
}

/* ----------------------------
answerErrorページの処理
----------------------------- */
class AnswerErrorPage {
  pageId = "#answerError";

  constructor() {
    const againBtn = document.querySelector(this.pageId + ' .js-answerError-again');
    againBtn.addEventListener('click', () => {
      pageChanger('answer')
    });
  }

  toAnswerErrorPage(message) {
    document.querySelector(this.pageId + ' .js-answerError-alert').textContent = message;
    pageViewChanger('answerError');
  }
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
const pageChanger = (pageId, message) => {

  switch (pageId) {
    case 'top':
      topPage.toTopPage();
      break;
    case 'problem':
      problemPage.toProblemPage();
      break;
    case 'answer':
      answerPage.toAnswerPage(message);
      break
    case 'problemError':
      problemErrorPage.toProblemErrorPage(message);
      break
    case 'answerError':
      answerErrorPage.toAnswerErrorPage(message);
      break
    default:
      console.error(pageId + 'というページは存在しません。');
      break;

  }
}