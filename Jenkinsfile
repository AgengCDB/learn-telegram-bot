pipeline {
  agent any

  stages {
    stage('Install dependencies') {
      steps {
        sh 'pip install -r requirements.txt || pip install python-telegram-bot'
      }
    }

    stage('Basic check') {
      steps {
        sh 'python -m py_compile main.py'
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
