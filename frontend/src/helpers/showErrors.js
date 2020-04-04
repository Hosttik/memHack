import showNotify from './showNotify';

const showErrors = (errors) => {
  if (errors && errors.length) {
    for (error of errors) {
      showNotify({
        text: error,
        type: 'error'
      })
    }
  } else {
    showNotify({
      text: 'Произошла ошибка',
      type: 'error'
    })
  }
};

export default showErrors;
