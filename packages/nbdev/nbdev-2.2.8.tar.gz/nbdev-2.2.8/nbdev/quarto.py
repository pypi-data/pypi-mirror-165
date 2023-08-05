# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/09_API/13_quarto.ipynb.

# %% ../nbs/09_API/13_quarto.ipynb 2
from __future__ import annotations
import warnings

from .config import *
from .doclinks import *

from fastcore.utils import *
from fastcore.script import call_parse
from fastcore.shutil import rmtree,move
from fastcore.meta import delegates

from os import system
import subprocess,sys,shutil,ast

# %% auto 0
__all__ = ['BASE_QUARTO_URL', 'install_quarto', 'install', 'nbdev_sidebar', 'nbdev_readme', 'prepare', 'refresh_quarto_yml',
           'nbdev_quarto', 'preview', 'deploy']

# %% ../nbs/09_API/13_quarto.ipynb 5
def _sprun(cmd):
    try: subprocess.check_output(cmd, shell=True)
    except subprocess.CalledProcessError as cpe: sys.exit(cpe.returncode)

# %% ../nbs/09_API/13_quarto.ipynb 7
BASE_QUARTO_URL='https://www.quarto.org/download/latest/'

def _install_linux():
    system(f'curl -LO {BASE_QUARTO_URL}quarto-linux-amd64.deb')
    system('sudo dpkg -i *64.deb && rm *64.deb')
    
def _install_mac():
    system(f'curl -LO {BASE_QUARTO_URL}quarto-macos.pkg')
    system('sudo installer -pkg quarto-macos.pkg -target /')

@call_parse
def install_quarto():
    "Install latest Quarto on macOS or Linux, prints instructions for Windows"
    if sys.platform not in ('darwin','linux'):
        return print('Please visit https://quarto.org/docs/get-started/ to install quarto')
    print("Installing or upgrading quarto -- this requires root access.")
    system('sudo touch .installing')
    try:
        installing = Path('.installing')
        if not installing.exists(): return print("Cancelled. Please download and install Quarto from quarto.org.")
        if 'darwin' in sys.platform: _install_mac()
        elif 'linux' in sys.platform: _install_linux()
    finally: system('sudo rm -f .installing')

# %% ../nbs/09_API/13_quarto.ipynb 8
@call_parse
def install():
    "Install Quarto and the current library"
    install_quarto.__wrapped__()
    d = get_config().path('lib_path')
    if (d/'__init__.py').exists(): system(f'pip install -e "{d.parent}[dev]"')

# %% ../nbs/09_API/13_quarto.ipynb 10
def _doc_paths(path:str=None, doc_path:str=None):
    cfg = get_config()
    cfg_path = cfg.config_path
    path = cfg.path('nbs_path') if not path else Path(path)
    doc_path = cfg.path('doc_path') if not doc_path else Path(doc_path)
    tmp_doc_path = path/f"{cfg['doc_path']}"
    return cfg,cfg_path,path,doc_path,tmp_doc_path

# %% ../nbs/09_API/13_quarto.ipynb 11
def _f(a,b): return Path(a),b
def _pre(p,b=True): return '    ' * (len(p.parts)) + ('- ' if b else '  ')
def _sort(a):
    x,y = a
    if y.startswith('index.'): return x,'00'
    return a

# %% ../nbs/09_API/13_quarto.ipynb 12
_def_file_re = '\.(?:ipynb|qmd|html)$'

# %% ../nbs/09_API/13_quarto.ipynb 13
@delegates(nbglob_cli)
def _nbglob_docs(
    path:str=None, # Path to notebooks
    file_glob:str=None, # Only include files matching glob    
    file_re:str=_def_file_re, # Only include files matching regex
    **kwargs):
    return nbglob(path, file_glob=file_glob, file_re=file_re, **kwargs)

# %% ../nbs/09_API/13_quarto.ipynb 14
@call_parse
@delegates(_nbglob_docs)
def nbdev_sidebar(
    path:str=None, # Path to notebooks
    printit:bool=False,  # Print YAML for debugging
    force:bool=False,  # Create sidebar even if settings.ini custom_sidebar=False
    skip_folder_re:str='(?:^[_.]|^www$)', # Skip folders matching regex
    **kwargs):
    "Create sidebar.yml"
    if not force and str2bool(get_config().custom_sidebar): return
    path = get_config().path('nbs_path') if not path else Path(path)
    files = nbglob(path, func=_f, skip_folder_re=skip_folder_re, **kwargs).sorted(key=_sort)
    lastd,res = Path(),[]
    for dabs,name in files:
        drel = dabs.relative_to(path)
        d = Path()
        for p in drel.parts:
            d /= p
            if d == lastd: continue
            title = re.sub('^\d+_', '', d.name)
            res.append(_pre(d.parent) + f'section: {title}')
            res.append(_pre(d.parent, False) + 'contents:')
            lastd = d
        res.append(f'{_pre(d)}{d.joinpath(name)}')

    yml_path = path/'sidebar.yml'
    yml = "website:\n  sidebar:\n    contents:\n"
    yml += '\n'.join(f'      {o}' for o in res)
    if printit: return print(yml)
    yml_path.write_text(yml)

# %% ../nbs/09_API/13_quarto.ipynb 17
def _render_readme(cfg_path, path, chk_time):
    idx_path = path/get_config().readme_nb
    if not idx_path.exists(): return
    readme_path = cfg_path/'README.md'
    if chk_time and readme_path.exists() and readme_path.stat().st_mtime>=idx_path.stat().st_mtime: return

    yml_path = path/'sidebar.yml'
    moved=False
    if yml_path.exists():
        # move out of the way to avoid rendering whole website
        yml_path.rename(path/'sidebar.yml.bak')
        moved=True
    try:
        _sprun(f'cd "{path}" && quarto render "{idx_path}" -o README.md -t gfm --no-execute')
    finally:
        if moved: (path/'sidebar.yml.bak').rename(yml_path)

# %% ../nbs/09_API/13_quarto.ipynb 18
@call_parse
def nbdev_readme(
    path:str=None, # Path to notebooks
    doc_path:str=None, # Path to output docs
    chk_time:bool=False): # Only build if out of date
    "Render README.md from index.ipynb"
    cfg,cfg_path,path,doc_path,tmp_doc_path = _doc_paths(path, doc_path)
    _render_readme(cfg_path, path, chk_time)
    if (tmp_doc_path/'README.md').exists():
        _rdm = cfg_path/'README.md'
        _rdmi = tmp_doc_path/(Path(get_config().readme_nb).stem + '_files')
        if _rdm.exists(): _rdm.unlink() # py37 doesn't have arg missing_ok so have to check first
        move(tmp_doc_path/'README.md', cfg_path) # README.md is temporarily in nbs/_docs
        if _rdmi.exists(): move(_rdmi, cfg_path) # Move Supporting files for README

# %% ../nbs/09_API/13_quarto.ipynb 19
@call_parse
def prepare():
    "Export, test, and clean notebooks, and render README if needed"
    import nbdev.test, nbdev.clean
    nbdev_export.__wrapped__()
    nbdev.test.nbdev_test.__wrapped__()
    nbdev.clean.nbdev_clean.__wrapped__()
    nbdev_readme.__wrapped__(chk_time=True)

# %% ../nbs/09_API/13_quarto.ipynb 20
def _ensure_quarto():
    if shutil.which('quarto'): return
    print("Quarto is not installed. We will download and install it for you.")
    install.__wrapped__()

# %% ../nbs/09_API/13_quarto.ipynb 21
_quarto_yml="""ipynb-filters: [nbdev_filter]

project:
  type: website
  output-dir: {doc_path}
  preview:
    port: 3000
    browser: false

format:
  html:
    theme: cosmo
    css: styles.css
    toc: true
    toc-depth: 4

website:
  title: "{title}"
  site-url: "{doc_host}{doc_baseurl}"
  description: "{description}"
  twitter-card: true
  open-graph: true
  reader-mode: true
  repo-branch: {branch}
  repo-url: "{git_url}"
  repo-actions: [issue]
  navbar:
    background: primary
    search: true
    right:
      - icon: github
        href: "{git_url}"
  sidebar:
    style: "floating"

metadata-files: 
  - sidebar.yml
  - custom.yml
"""

# %% ../nbs/09_API/13_quarto.ipynb 22
def refresh_quarto_yml():
    "Generate `_quarto.yml` from `settings.ini`."
    cfg = get_config()
    p = cfg.path('nbs_path')/'_quarto.yml'
    vals = {k:cfg.get(k) for k in ['doc_path', 'title', 'description', 'branch', 'git_url', 'doc_host', 'doc_baseurl']}
    # Do not build _quarto_yml if custom_quarto_yml is set to True
    if str2bool(get_config().custom_quarto_yml): return
    if 'title' not in vals: vals['title'] = vals['lib_name']
    yml=_quarto_yml.format(**vals)
    p.write_text(yml)

# %% ../nbs/09_API/13_quarto.ipynb 23
def _is_qpy(path:Path):
    "Is `path` a py script starting with frontmatter?"
    path = Path(path)
    if not path.suffix=='.py': return
    try: p = ast.parse(path.read_text())
    except: return
    if not p.body: return
    a = p.body[0]
    if isinstance(a, ast.Expr) and isinstance(a.value, ast.Constant):
        v = a.value.value.strip().splitlines()
        return v[0]=='---' and v[-1]=='---'

# %% ../nbs/09_API/13_quarto.ipynb 24
def _exec_py(fname):
    "Exec a python script and warn on error"
    try: subprocess.check_output('python ' + fname, shell=True)
    except subprocess.CalledProcessError as cpe: warn(str(cpe))

# %% ../nbs/09_API/13_quarto.ipynb 25
@call_parse
@delegates(_nbglob_docs)
def nbdev_quarto(
    path:str=None, # Path to notebooks
    doc_path:str=None, # Path to output docs
    preview:bool=False, # Preview the site instead of building it
    file_glob:str=None, # Only include files matching glob    
    port:int=3000, # The port on which to run preview
    **kwargs):
    "Create Quarto docs and README.md"
    _ensure_quarto()
    import nbdev.doclinks
    nbdev.doclinks._build_modidx(skip_exists=True)
    cfg,cfg_path,path,doc_path,tmp_doc_path = _doc_paths(path, doc_path)
    refresh_quarto_yml()
    nbdev_sidebar.__wrapped__(path, file_glob=file_glob, **kwargs)
    pys = globtastic(path, file_glob='*.py', **kwargs).filter(_is_qpy)
    for py in pys: _exec_py(py)
    if preview: os.system(f'cd "{path}" && quarto preview --port {port}')
    else: 
        nbdev_readme.__wrapped__(path, doc_path) # README must be generated BEFORE render because of how index.html is generated by Quarto
        _sprun(f'cd "{path}" && quarto render --no-cache')
        if tmp_doc_path.parent != cfg_path: # move docs folder to root of repo if it doesn't exist there
            rmtree(doc_path, ignore_errors=True)
            move(tmp_doc_path, cfg_path)

# %% ../nbs/09_API/13_quarto.ipynb 26
@call_parse
@delegates(nbdev_quarto, but=['preview'])
def preview(
    path:str=None, # Path to notebooks
    **kwargs):
    "Preview docs locally"
    os.environ['QUARTO_PREVIEW']='1'
    nbdev_quarto.__wrapped__(path, preview=True, **kwargs)

# %% ../nbs/09_API/13_quarto.ipynb 27
@call_parse
@delegates(nbdev_quarto)
def deploy(
    path:str=None, # Path to notebooks
    skip_build:bool=False,  # Don't build docs first
    **kwargs):
    "Deploy docs to GitHub Pages"
    if not skip_build: nbdev_quarto.__wrapped__(path, **kwargs)
    try: from ghp_import import ghp_import
    except: return warnings.warn('Please install ghp-import with `pip install ghp-import`')
    ghp_import(get_config().path('doc_path'), push=True, stderr=True, no_history=True)
