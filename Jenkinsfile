pipeline {
  agent any
  environment {
    CI = 'true'
  }
  stages {
    stage('Build') {
      steps {
        echo "Installing package requirements and building container"
        sh 'docker build . --tag siegeanalyzer --build-arg SIEGEANALYZERTOKEN=$SIEGEANALYZERTOKEN --build-arg POSTGRESHOST=$POSTGRESHOST --build-arg SIEGEANALYZERDATABASE=$SIEGEANALYZERDATABASE --build-arg SIEGEANALYZERDBUSER=$SIEGEANALYZERDBUSER --build-arg SIEGEANALYZERDBPASS=$SIEGEANALYZERDBPASS --build-arg POSTGRESPORT=$POSTGRESPORT'
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
        sh 'sshpass -p $STRATMAPPERPASSWORD rsync -avzP $WORKSPACE/ stratmapper@$SERVER:$STRATMAPPERLOCATION/'
        sh 'sshpass -p $STRATMAPPERPASSWORD ssh -oStrictHostKeyChecking=no stratmapper@$SERVER "(cd $STRATMAPPERLOCATION/ && docker-compose down)"'
        sh 'sshpass -p $STRATMAPPERPASSWORD ssh -oStrictHostKeyChecking=no stratmapper@$SERVER "(cd $STRATMAPPERLOCATION/ && docker-compose up --build -d)"'
      }
    }
  }
}