import glob
import sys
from importlib import reload

def fetch_configs(data):
  projects = {}
  sys.path.insert(0, 'config/projects/')
  for project_config_location in glob.glob("config/projects/*.py"):
    try: 
      filename = project_config_location.split("/")[-1].replace(".py", "")
      project_module = __import__(filename)
      reload(project_module)
      projects[project_module.get_name()] = project_module.get_config()
    except Exception as e:
        print(f'Failed to parse {project_config_location}: {e}')
  chains = {}
  sys.path.insert(0, 'config/chains/')
  for chain_config_location in glob.glob("config/chains/*.py"):
    try:
      filename = chain_config_location.split("/")[-1].replace(".py", "")
      chain_module = __import__(filename)
      reload(chain_module)
      chains[chain_module.get_name()] = chain_module.get_config()
    except Exception as e:
        print(f'Failed to parse {chain_config_location}: {e}')
  
  # Check if the project exists
  project_id = data['project_id']
  if project_id not in projects:
    print(f"Project '{project_id}' not found. Available projects: {list(projects.keys())}")
    raise ValueError(f"Project '{project_id}' not found")
    
  project = projects[project_id]
  
  # Check if the chain exists
  chain_name = project['chain']
  if chain_name not in chains:
    print(f"Chain '{chain_name}' not found. Available chains: {list(chains.keys())}")
    raise ValueError(f"Chain '{chain_name}' not found")
    
  chain = chains[chain_name]
  project['parallel'] = data.get('parallel', False)
  project['lp_summary'] = data.get('lp_summary', False)
  project['hide_no_rewards'] = data.get('hide_no_rewards', False)

  print_all(chains, projects)

  return chain, project
  
def print_all(chains, projects):
  project_list = "Projects: "
  for project in projects.keys():
    project_list += project + ", "
  print(project_list[0:-2])
  print(" ")
  chain_list = "Chains: "
  for chain in chains.keys():
    chain_list += chain + ", "
  print(chain_list[0:-2])