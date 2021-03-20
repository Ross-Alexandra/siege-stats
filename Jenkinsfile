pipeline {
  agent any
  environment {
    CI = 'true'
  }
  stages {
    stage('Build') {
      steps {
        echo "Test installing package requirements and building container"
        sh 'docker build . --tag siegeanalyzer_$BRANCH_NAME --build-arg SIEGEANALYZERTOKEN=$SIEGEANALYZERTOKEN --build-arg POSTGRESHOST=$POSTGRESHOST --build-arg SIEGEANALYZERDATABASE=$SIEGEANALYZERDATABASE --build-arg SIEGEANALYZERDBUSER=$SIEGEANALYZERDBUSER --build-arg SIEGEANALYZERDBPASS=$SIEGEANALYZERDBPASS --build-arg POSTGRESPORT=$POSTGRESPORT'
      }
    }
    stage('Test') {
      steps {
        echo 'Test'
      }
    }
    stage('Cleanup') {
        steps {
            echo 'Cleanup'
        }
    }
    stage('Master-Deploy') {
      when {
        expression { env.BRANCH_NAME == 'master' }
      }
      steps {
        sh 'sshpass -p $ANALYSISBOTPASSWORD rsync -avzP $WORKSPACE/ analysisbot@$SERVER:$SIEGEANALYZERLOCATION/'
        sh 'sshpass -p $ANALYSISBOTPASSWORD ssh -oStrictHostKeyChecking=no analysisbot@$SERVER "(cd $SIEGEANALYZERLOCATION/ && docker stop siegeanalyzer && docker rm siegeanalyzer)"'
        sh 'sshpass -p $ANALYSISBOTPASSWORD ssh -oStrictHostKeyChecking=no analysisbot@$SERVER "(cd $SIEGEANALYZERLOCATION/ && docker build . --tag siegeanalyzer --build-arg SIEGEANALYZERTOKEN=$SIEGEANALYZERTOKEN --build-arg POSTGRESHOST=$POSTGRESHOST --build-arg SIEGEANALYZERDATABASE=$SIEGEANALYZERDATABASE --build-arg SIEGEANALYZERDBUSER=$SIEGEANALYZERDBUSER --build-arg SIEGEANALYZERDBPASS=\'$SIEGEANALYZERDBPASS\' --build-arg POSTGRESPORT=$POSTGRESPORT)"'
        sh 'sshpass -p $ANALYSISBOTPASSWORD ssh -oStrictHostKeyChecking=no analysisbot@$SERVER "(cd $SIEGEANALYZERLOCATION/ && docker run -d --name siegeanalyzer siegeanalyzer)"'
      }
    }
  }
}
