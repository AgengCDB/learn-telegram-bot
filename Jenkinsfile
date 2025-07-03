pipeline {
  agent {
    docker {
      image 'python:3.10-slim'
    }
  }

  environment {
    VENV_PATH = '.venv'
  }

  stages {
    stage('Setup venv') {
      steps {
        sh '''
          python -m venv $VENV_PATH
          . $VENV_PATH/bin/activate
          pip install --upgrade pip
          pip install -r requirements.txt || pip install python-telegram-bot
        '''
      }
    }

    stage('Check syntax') {
      steps {
        sh '. $VENV_PATH/bin/activate && python -m py_compile bot.py'
      }
    }
  }

  post {
    success { echo '✅ All good!' }
    failure { echo '❌ Fix issues and try again.' }
  }
}
