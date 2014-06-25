# Ansible Lookup Plugin: OS Specific

This lookup plugin allows to define a list of items with os or distribution specific overrides.

## Motivation

I wrote the plugin because I don't like to have a task list like the following:

	- name: copy file for Archlinux
	  copy: src=Archlinux/foo dst=/destination/on/Archlinux
	  when: ansible_os_family == 'Archlinux'

	- name: copy file for Debian
	  copy: src=Debian/foo dst=/destination/on/Debian
	  when: ansible_os_family == 'Debian'

The result of this is that I have a skipping task on each run and it gets worse if more systems are added.

One solution to this "problem" would be to just load os specific variable files, e.g.:

	- name: load variables
	  include_vars: "{{ item }}"
	  with_first_found:
	  	- "{{ ansible_distribution }}-{{ ansible_distribution_version }}.yml"
	  	- "{{ ansible_distribution }}-{{ ansible_distribution_major_version }}.yml"
	  	- "{{ ansible_distribution }}-{{ ansible_distribution_release }}.yml"
	  	- "{{ ansible_distribution }}.yml"
	  	- "{{ ansible_os_family }}.yml"
	  	- "default.yml"

	 - name: copy file
	   copy: src={{ item.src }} dst={{ item.dst }}
	   with_items: loaded_file_list

But this is obscure and you have to duplicate common items across multiple files which may be difficult to maintain.

## Usage

This plugin allows the following:

	- name: copy file
	  copy: src={{ item.src }} dst={{ item.dst }}
	  with_os_specific:
	  	- { src: some-common-file, dst: /some-common-destination }
	  	- default: { src: fallback-file, dst: /default-destination }
	  	  Debian: { src: debian-file, dst: /debian-destination }
	  	- Debian: { src: debian-only-file, dst: /debian-only-destination }

The first item will be selected on each system.
The second item defines a default case for systems other than `Debian` and a specific case for `Debian` systems.
The third item defines no default case and is only defined for `Debian` systems.

So, on `Debian` there are three files copied to the target host, on all other systems just two.
If the filtered list results in an empty list, the task is marked as skipped.

While it may be a bit confusing at first, I really like it to write my tasks this way.

## Installation

Simply clone this repository and create a symlink inside a directory `lookup_plugins` in the same directory of your playbook.
If you are using git for your playbook, for example, you can add this as a submodule:

	git submodule add https://github.com/mantiz/ansible-lookup-plugin-os-specific external/lookup-plugin-os-specific
	mkdir lookup_plugins
	ln -s ../external/lookup-plugin-os-specific/os_specific.py lookup_plugins

## Lookup priorities

If the item is just a string, the item will be taken as it is.
If it is a dictionary, the following priorities apply:

1. `<ansible_distribution>-<ansible_distribution_version>` (e.g. `Ubuntu-12.04`)
2. `<ansible_distribution>-<ansible_distribution_major_version>` (e.g. `Ubuntu-12`)
3. `<ansible_distribution>-<ansible_distribution_release>` (e.g. `Ubuntu-precise`)
4. `<ansible_distribution>` (e.g. `Ubuntu`)
5. `<ansible_os_family>` (e.g. `Ubuntu`)
   I really don't know in which cases `ansible_distribution` differs from `ansible_os_family` but there may be cases where this is needed.
6. `default`
