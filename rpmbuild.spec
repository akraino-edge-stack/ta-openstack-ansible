Name:           openstack-ansible
Version:        17.0.2
Release:        1%{?dist}.1
License:        %{_platform_licence} and ASL 2.0
Source0:        https://github.com/openstack/%{name}/archive/%{version}.tar.gz
Patch0:         0001-initial.patch
Vendor:         %{_platform_vendor} and OpenStack modified
URL:            https://github.com/openstack/openstack-ansible
BuildArch:      noarch
Summary:        openstack-ansible
Requires:       openstack-ansible

%description
openstack-ansible

%prep
%autosetup -n %{name}-%{version} -p 1

%build

%install
mkdir -p %{buildroot}/opt/openstack-ansible
rsync -av --exclude LICENSE --exclude rpmbuild.spec --exclude inventory/env.d/ --exclude .git/ --exclude .gitreview --exclude .eggs/ . %{buildroot}/opt/openstack-ansible/
mkdir -p %{buildroot}/usr/local/bin/
cp -f scripts/openstack-ansible %{buildroot}/usr/local/bin/openstack-ansible
cp -f scripts/openstack-ansible.rc %{buildroot}/usr/local/bin/openstack-ansible.rc
cp -f scripts/setup-controller.sh %{buildroot}/usr/local/bin/
# Create a dummy directory for role pip_install,apt_package_pinning are dependencies for some roles.
# They are anyway masked with --skip-tags option while running ansible.
mkdir -p %{buildroot}/etc/ansible/roles/etcd
mkdir -p %{buildroot}/etc/ansible/roles/bird
mkdir -p %{buildroot}/etc/ansible/roles/pip_install
mkdir -p %{buildroot}/etc/ansible/roles/apt_package_pinning
mkdir -p %{buildroot}%_bootstrapping_path
mkdir -p %{buildroot}%_provisioning_path
mkdir -p %{buildroot}%_postconfig_path

%files
/opt/openstack-ansible
%attr(0755, root, root) /usr/local/bin/openstack-ansible
%attr(0755, root, root) /usr/local/bin/setup-controller.sh
/usr/local/bin/openstack-ansible.rc
/etc/ansible/roles/etcd
/etc/ansible/roles/bird
/etc/ansible/roles/pip_install
/etc/ansible/roles/apt_package_pinning
%_bootstrapping_path
%_provisioning_path
%_postconfig_path


%post
ln -s /opt/openstack-ansible/playbooks/galera-install.yml %_bootstrapping_path
ln -s /opt/openstack-ansible/playbooks/rabbitmq-install.yml %_bootstrapping_path
ln -s /opt/openstack-ansible/playbooks/rsyslog-install.yml %_bootstrapping_path
ln -s /opt/openstack-ansible/playbooks/os-ironic-install.yml %_bootstrapping_path

ln -s /opt/openstack-ansible/playbooks/ntp-config.yml %_bootstrapping_path
ln -s /opt/openstack-ansible/playbooks/ntp-config.yml %_provisioning_path

#postconfig
ln -s /opt/openstack-ansible/playbooks/galera-install.yml %_postconfig_path
ln -s /opt/openstack-ansible/playbooks/memcached-install.yml %_postconfig_path
ln -s /opt/openstack-ansible/playbooks/rabbitmq-install.yml %_postconfig_path
ln -s /opt/openstack-ansible/playbooks/rsyslog-install.yml %_postconfig_path
ln -s /opt/openstack-ansible/playbooks/haproxy-install.yml %_postconfig_path
ln -s /opt/openstack-ansible/playbooks/hosts_config.yml %_postconfig_path
ln -s /opt/openstack-ansible/playbooks/os-ironic-install.yml %_postconfig_path
ln -s /opt/openstack-ansible/playbooks/os-keystone-install.yml %_postconfig_path

mkdir -p %_platform_etc_path/required-secrets
cp -f /opt/openstack-ansible/etc/openstack_deploy/user_secrets.yml %_platform_etc_path/required-secrets/000-user_secrets.yml

%postun
