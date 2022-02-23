import subprocess
import os
import yaml

filename = 'users.yml'
path_to_keys = '/var/run/work_keys/'
path_home_dir = '/home/'

create_dir = os.mkdir(path_to_keys)
get_git_key = subprocess.run(["git", "clone", "git@github.com:renvissvnce/work_keys.git", path_to_keys])

# show linux users
user_linux = os.listdir(path_home_dir)
# show pub keys
create_list_of_users = [f for f in os.listdir(path_to_keys) if not f.startswith('.')]


def write_file(file):
    yaml_user_dict = dict()

    for linux_username in create_list_of_users:
        if linux_username in ['gisops', 'video0']:
            pass
        else:
            converting = linux_username.split('.pub')[0]
            path_to_file = path_to_keys + linux_username
            yaml_user_dict[converting] = path_to_file

    with open(file, 'w') as f:
        data = {
            'create users': yaml_user_dict,
            'don\'t delete user': ['gisops', 'video0', '.git']
        }
        yaml.dump(data, f)

write_file(filename)


def run_sudo_usr(command: list):
    for i in command:
        run_cmd_usr = subprocess.run(i)

        if run_cmd_usr.returncode == 0:
            print('Step {} - ok'.format(i))
        else:
            print('Step {} - something is wrong'.format(i))


def get_cmd(username):
    path = path_home_dir + username + '/.ssh/'
    home_path = os.path.join(path)
    add_usr = ['useradd', '-m', username]
    delete_passwd = ['passwd', '-d', username]
    dir_ssh = ['mkdir', home_path]
    change_owner = ['chown', '-R', username, home_path]
    change_mode = ['chmod', '700', home_path]
    auth_key = ['cp', path_to_keys + username + '.pub', home_path + 'authorized_keys']
    cmd_create_user = [add_usr, delete_passwd, dir_ssh, change_owner, change_mode, auth_key]
    return cmd_create_user


def check_user_list():
    with open(filename) as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
        users = data['don\'t delete user']
        create_users = data['create users']
        all_items = create_users.items()

        for key_username in all_items:
            converted = key_username[0]
            if converted + '.py' in user_linux:
                print('just pass this iteration, user - [{}], already created.'.format(converted))
            elif converted not in user_linux:
                print('create user {}'.format(converted))
                run_sudo_usr(get_cmd(converted))

        for i in users:
            if i in users:
                print('pass this iterations, I can\'t delete it')
            elif i + '.pub' not in users:
                print('delete user {}'.format(i))
                deleting_user = subprocess.run(['sudo', 'userdel', '{i}'])
                delete_dir = subprocess.run(['sudo', 'rm', '-r', '/home/{i}'])


check_user_list()
