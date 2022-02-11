import subprocess
import os
import yaml

filename = 'users.yml'

create_dir = subprocess.run(["mkdir", "/var/run/work_keys"])
get_git_key = subprocess.run(["git", "clone", "git@github.com:renvissvnce/work_keys.git", "/var/run/work_keys"])

cmd = ['ls /var/run/work_keys/']
cmd_usr = ['ls /home/']

# show linux users
user_linux = subprocess.check_output(cmd_usr, shell=True)
list_user_linux = user_linux.decode().splitlines()
# show pub keys
create_list_of_users = subprocess.check_output(cmd, shell=True)
user_list_decode = create_list_of_users.decode().splitlines()



def add_new_user_yaml():
    for_keys = []
    for_values = []
    yaml_user_dict = dict()

    for linux_username in user_list_decode:
        if linux_username in ['gisops', 'video0']:
            pass
        else:
            converting = linux_username.split('.py')[0]
            for_keys.append(converting)

    for paths_to_key in user_list_decode:
        for_values.append('/var/run/work_keys/'+paths_to_key)

    for items in range(len(for_keys)):
        yaml_user_dict[for_keys[items]] = for_values[items]

    return yaml_user_dict


def write_file(file):
    with open(file, 'w') as f:
        data = {
            'create users': add_new_user_yaml(),
            'don\'t delete user': ['gisops', 'video0']
                }
        yaml.dump(data, f)
write_file(filename)

# проверка на создание пользователя или удаление


def run_sudo_usr(command: list):
    for i in command:
        run_cmd_usr = subprocess.run(i)

        if run_cmd_usr.returncode == 0:
            print('Step {} - ok'.format(i))
        else:
            print('Step {} - something is wrong'.format(i))


for git_username in user_list_decode:
    username = git_username.split('.pub')
    path = '/home/' + username[0] + '/.ssh/'
    home_path = os.path.join(path)
    add_usr = ['useradd', '-m', username[0]]
    delete_passwd = ['passwd', '-d', username[0]]
    dir_ssh = ['mkdir', home_path]
    change_owner = ['chown', '-R', username[0], home_path]
    change_mode = ['chmod', '700', home_path]
    auth_key = ['cp', '/var/run/work_keys/' + git_username, home_path + 'authorized_keys']
    cmd_create_user = [add_usr, delete_passwd, dir_ssh, change_owner, change_mode, auth_key]


def check_user_list():

    with open(filename) as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
        users = data['don\'t delete user']
        create_users = data['create users']
        all_items = create_users.items()

        for key_username in all_items:
            converted = key_username[0]
            if converted + '.py' in list_user_linux:
                print('just pass this iteration, user - [{}], already created.'.format(converted))
            elif converted not in list_user_linux:
                print('create user {}'.format(converted))
                run_sudo_usr(cmd_create_user)

        for i in users:
            if i in users:
                print('pass this iterations, I can\'t delete it')
            elif i + '.pub' not in users:
                print('delete user {}'.format(i))
                deleting_user = subprocess.run(['sudo', 'userdel', '{i}'])
                delete_dir = subprocess.run(['sudo', 'rm', '-r', '/home/{i}'])


check_user_list()
