from diagrams import Cluster, Diagram, Edge
from diagrams.onprem.ci import Jenkins
from diagrams.onprem.client import Users
from extensions.onprem_extensions import Stash, SonarQube, DockerNodejs, BosDevArtifactory, NPM, Scheduler
from diagrams.aws.storage import S3
from diagrams.saas.chat import Slack
from utils.constants import Colors

with Diagram(name="UI Automation", show=True, filename="ui_automation"):
    users = Users("Users")
    stash = Stash("Stash repo")

    with Cluster("Internet"):
        slack = Slack("Slack Channels")

    with Cluster("AWS"):
        s3 = S3("S3 Bucket")

    with Cluster("Bosdev Artifactory"):
        artifactory = BosDevArtifactory("Artifactory")

    npm_pkg = NPM("eze-integration-protractor-framework")
    npm_pkg_e2e = NPM("eze-e2e-* packages")

    with Cluster("Jenkins Server"):
        scheduler = Scheduler("cron scheduler")
        jenkins = Jenkins("UI Automation Build/Publish")
        with Cluster("Build/publish"):
            jenkins_builds = [
                Jenkins("Build"),
                Jenkins("Publish"),
                Jenkins("Upload framework")
            ]
        with Cluster("Test Builds"):
            jenkins_test_builds = [
                Jenkins("Castle Smoke Tests"),
                Jenkins("AWS Prod Smoke Tests"),
                Jenkins("Post Deployment Tests"),
                Jenkins("DevRoute Tests"),
                Jenkins("Chrome Beta"),
            ]
        scheduler >> [
            jenkins_test_builds[0],
            jenkins_test_builds[1],
            jenkins_test_builds[3],
            jenkins_test_builds[4]
        ]
        jenkins >> jenkins_builds
        jenkins_builds[1] >> npm_pkg >> Edge(label="Publishes npm package") >> artifactory
        jenkins_builds[2] >> Edge(label="Upload framework as .zip") >> s3
        jenkins_test_builds >> Edge(color=Colors.DARK_ORANGE) >> slack
        jenkins_test_builds >> Edge(color=Colors.DARK_GREEN) >> s3
        artifactory >> Edge(color=Colors.FIRE_BRICK) >> jenkins_test_builds
        npm_pkg_e2e >> Edge(label="Teams publish eze-e2e-* packages") >> artifactory
        artifactory >> Edge(color=Colors.BLUE) >> jenkins_test_builds

    with Cluster("Rancher Infrastructure"):
        with Cluster("SonarQube Stack"):
            sonar = SonarQube("SonarQube")
            jenkins_builds[0] >> Edge(label="Sonar scan analysis") >> sonar

        with Cluster("ITTS Service"):
            itts = DockerNodejs('ITTS')
            itts >> jenkins_test_builds[2]

    users >> Edge(label="Merge Changes") >> stash
    stash >> Edge(label="Triggers build") >> jenkins