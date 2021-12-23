from diagrams import Diagram, Cluster, Edge
from extensions.onprem_extensions import DockerNodejs, Scheduler
from diagrams.onprem.ci import Jenkins
from diagrams.onprem.security import Vault
from diagrams.aws.storage import S3
from diagrams.saas.chat import Slack

from diagrams.aws.compute import EC2
from diagrams.aws.database import RDS
from diagrams.aws.network import ELB


with Diagram("Integration Test Trigger Service", show=False):

  vault = Vault("Vault Castle")

  with Cluster("AWS"):
    config = S3("S3 Bucket")
  
  with Cluster("Jenkins"):
    with Cluster("Product Teams"):
      pd_teams_ui = Jenkins("Team UI Tests")
      pd_teams_api = Jenkins("Team API Tests")

    with Cluster("IQA"):
      pd_ui = Jenkins("PD UI Tests")
      pd_api = Jenkins("PD API Tests")
      dr = Jenkins("DevRoute Tests")
    
    pd_teams_ui >> Edge(label="trigger downstream job") >> pd_ui
    pd_teams_api >> Edge(label="trigger downstream job") >> pd_api

  with Cluster("Internet"):
    slack = Slack("Slack Channels")
  
  with Cluster("Rancher"):
    with Cluster("ITTS"):
      scheduler = Scheduler("cron scheduler")
      itt = DockerNodejs("ITTS")
      itt - scheduler
    
    audit = DockerNodejs("Audit Service")
    scheduler >> Edge(label="monitor deployments in castle") >> audit
  
  vault << Edge(label="read secrets") << itt
  scheduler >> Edge(label="read configuration files") >> config
  scheduler >> Edge(label="send slack messages") >> slack
  scheduler >> Edge(label="trigger job") >> [pd_teams_ui, pd_teams_api, dr]