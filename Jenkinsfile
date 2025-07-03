pipeline {
  agent {
    docker {
      image 'python:3.10-slim'
    }
  }

  stages {
    stage('Install dependencies') {
      steps {
        sh '''
          pip install --upgrade pip
          pip install -r requirements.txt || pip install python-telegram-bot
        '''
      }
    }

    stage('Basic check') {
      steps {
        sh 'python -m py_compile bot.py'
      }
    }

    stage('Run (dry check)') {
      steps {
        echo '✅ Code looks OK. Not running bot in CI.'
      }
    }
  }

  post {
    success {
      echo '🎉 Build passed. Your Telegram bot code looks fine!'
    }
    failure {
      echo '❌ Build failed! Please fix syntax or dependency issues.'
    }
  }
}
