[Version 1.0.1 (2022-08-30)](https://pypi.org/project/ktpanda-firewall/1.0.1/)
============================

* Migrate to setup.cfg ([9bfc6b6](https://gitlab.com/ktpanda/firewall/-/commit/9bfc6b66718ba96a3dfc706dc27b4cb20f629f02))
* Author name change ([658c74c](https://gitlab.com/ktpanda/firewall/-/commit/658c74ce58dbe5968caaf76efa2f2660c67ef865))
* Rename package to python_firewall ([d7a2146](https://gitlab.com/ktpanda/firewall/-/commit/d7a2146d36d500385ed921dcd3361795ad3f6668))
* Fix mini_http ([06cf3fb](https://gitlab.com/ktpanda/firewall/-/commit/06cf3fbb7f5ee199bd63fd7fa96ec7f813a92407))
* Add missing files ([57ad161](https://gitlab.com/ktpanda/firewall/-/commit/57ad161aa22abb35b3c450ff31296a19f075392c))
* Update to Python 3 using asyncio ([4857a77](https://gitlab.com/ktpanda/firewall/-/commit/4857a77fdf3ccc1bbd246e2ae2daa4ac825eb968))


Version 1.0.0
=============

* Remove etc/ ([b2e90c9](https://gitlab.com/ktpanda/firewall/-/commit/b2e90c9ccff48ba455366b698d361bb4e0584c6c))
* Make shebang explicitly reference python2 ([199fab7](https://gitlab.com/ktpanda/firewall/-/commit/199fab7d9121113e9793ca41af16e51a50e53020))
* Add nat.dnat_loopback setting ([54734cc](https://gitlab.com/ktpanda/firewall/-/commit/54734cc7ec3326add174dca43a104d2b8c018f0a))
* Only jump to MASQ table for packets going out on wan interface ([941ade2](https://gitlab.com/ktpanda/firewall/-/commit/941ade25c26092efe6d2b90f0bc100c3a345dcaf))
* Add extra SNAT rules for forwarded ports so that users on the local network can use the public address for servers ([d17ea62](https://gitlab.com/ktpanda/firewall/-/commit/d17ea62390361a98d4d282a1b2c0dd0336b68eb3))
* Remove 'interface not found' messages ([8c4c3ba](https://gitlab.com/ktpanda/firewall/-/commit/8c4c3ba8a4ecd8ba72aed4ae2dacdafdda82ccfc))
* Initial commit ([26dfbc7](https://gitlab.com/ktpanda/firewall/-/commit/26dfbc7180cdfc92f3c3028d7da0cd2e3d80e9fe))
