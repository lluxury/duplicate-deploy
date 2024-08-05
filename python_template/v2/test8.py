from jinja2 import Environment, FileSystemLoader, select_autoescape

# 创建 Jinja2 环境
env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['j2'])
)

# 定义要渲染的模板文件
template = env.get_template('azure-pipeline.j2')

# 定义生成的 YAML 文件名称和渲染参数
yaml_files = [
    {
        'filename': 'azure-pipeline-production.yml',
        'deploy_to_production': True,
        'branches': ['main', 'development'],
        'imageName': 'myapp',
        'helmChartPath': './helm/charts/mychart',
        'additional_variables': {
            'ENVIRONMENT': 'production',
            'API_KEY': 'your_production_api_key'
        },
        'build_steps': [
            {'command': 'npm install', 'display_name': 'Install Dependencies'},
            {'command': 'npm run build', 'display_name': 'Build Project'}
        ]
    },
    {
        'filename': 'azure-pipeline.yml',
        'deploy_to_production': False,
        'branches': ['main'],
        'imageName': 'myapp',
        'helmChartPath': './helm/charts/mychart',
        'additional_variables': {
            'ENVIRONMENT': 'staging',
            'API_KEY': 'your_staging_api_key'
        },
        'build_steps': [
            {'command': 'npm install', 'display_name': 'Install Dependencies'},
            {'command': 'npm run build', 'display_name': 'Build Project'},
            {'command': 'npm test', 'display_name': 'Run Tests'}
        ]
    }
]

# 渲染并生成 YAML 文件
for entry in yaml_files:
    rendered_yaml = template.render(
        deploy_to_production=entry['deploy_to_production'],
        branches=entry['branches'],
        imageName=entry['imageName'],
        helmChartPath=entry['helmChartPath'],
        additional_variables=entry['additional_variables'],
        build_steps=entry['build_steps']
    )

    with open(entry['filename'], 'w') as f:
        f.write(rendered_yaml)

    print(f"Generated {entry['filename']} successfully.")

