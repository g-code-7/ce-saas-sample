pipeline {
    agent any

    environment {
        IMAGE = credentials('IMAGE')
        REPO = credentials('REPO')
        BRANCH = "main"
        GHCR_PAT = credentials('GHCR_PAT')
    }

    triggers {
        pollSCM('H/5 * * * *')
    }

    stages {

        stage('Clone Repo') {
            steps {
                checkout scm
            }
        }

        stage('Build & Push Image with Buildah') {
            steps {
                echo "Building image ${IMAGE} with Buildah and pushing to GHCR"
                sh '''
                # Login to GHCR
                echo $GHCR_PAT | buildah login -u your-username --password-stdin ghcr.io

                # Build the image from the Dockerfile
                buildah bud -f Dockerfile -t $IMAGE .

                # Push the image to GHCR
                buildah push $IMAGE
                '''
            }
        }

        stage('Deploy Pod to Kubernetes') {
            steps {
                echo "Creating pod using image ${IMAGE}"
                sh '''
                kubectl apply -f deployment.yml
                kubectl rollout restart deployment saas-deployment
                kubectl apply -f service.yml
                '''
            }
        }

        stage('Verify Pod') {
            steps {
                sh '''
                echo "Waiting 5 seconds for pod to start..."
                sleep 5
                kubectl get deployment | grep saas-deployment
                '''
            }
        }
    }
}