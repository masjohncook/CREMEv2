from interface import implements
from .interfaces import IConfiguration, IConfigurationCommon, IConfigurationAttack, IConfigurationBenign,\
    IDataCollection, IDataCentralization, IBenignReproduction, IMiraiAttackerServer, IMiraiMaliciousClient,\
    ICleaningBenignReproduction, ICleaningAttackReproduction, IConfigurationAttackerSide, IDiskWipeAttackerServer,\
    IRansomwareAttackerServer, IResourceHijackingAttackerServer, IEndPointDosAttackerServer, ICleaningDataCollection
from .helper import ScriptHelper, OtherHelper
from .CREME import Creme
import time


class Machine:
    show_cmd = False  # a flag use to show cmd or execute cmd

    # Controller's information
    controller_hostname = None
    controller_ip = None
    controller_username = None
    controller_password = None
    controller_path = None

    def __init__(self, hostname, ip, username, password, path):
        self.hostname = hostname
        self.ip = ip
        self.username = username
        self.password = password
        self.path = path

    def __str__(self):
        attrs = vars(self)
        return ', '.join("%s: %s" % item for item in attrs.items())


class DataLoggerServer(Machine, implements(IConfiguration), implements(IConfigurationCommon),
                       implements(IDataCollection), implements(IDataCentralization),
                       implements(ICleaningDataCollection)):

    def __init__(self, hostname, ip, username, password, path, network_interface, tcp_file="traffic.pcap",
                 tcp_pids_file="tcp_pids.txt", atop_interval=1, time_window_traffic=1):
        super().__init__(hostname, ip, username, password, path)
        self.path = path
        self.network_interface = network_interface
        self.tcp_file = tcp_file
        self.tcp_pids_file = tcp_pids_file
        self.atop_interval = atop_interval
        self.time_window_traffic = time_window_traffic

    def configure(self):
        self.configure_base()
        self.configure_data_collection()

    def configure_base(self):
        filename_path = "00_configuration/DataLogger/DataLoggerServer_base.sh"
        parameters = [self.ip, self.username, self.password]
        ScriptHelper.execute_script(filename_path, parameters, self.show_cmd)

    def configure_data_collection(self):
        filename_path = "00_configuration/DataLogger/DataLoggerServer_data_collection.sh"
        parameters = [self.ip, self.username, self.password, self.controller_ip, self.controller_username,
                      self.controller_password, self.controller_path]
        ScriptHelper.execute_script(filename_path, parameters, self.show_cmd)

    def start_collect_data(self):
        filename_path = "01_data_collection/start_packet.sh"
        parameters = [self.ip, self.username, self.password, self.path, self.tcp_file, self.network_interface,
                      self.tcp_pids_file]
        ScriptHelper.execute_script(filename_path, parameters, self.show_cmd)

    def stop_collect_data(self):
        filename_path = "04_general/kill_pids.sh"
        parameters = [self.ip, self.username, self.password, self.path, self.tcp_pids_file]
        ScriptHelper.execute_script(filename_path, parameters, self.show_cmd)

    def download_atop_data(self, data_logger_client):
        filename_path = "01_data_collection/download_atop_data.sh"
        parameters = [self.ip, self.username, self.password, data_logger_client.ip, data_logger_client.username,
                      data_logger_client.password, data_logger_client.path, data_logger_client.atop_file, self.path]
        ScriptHelper.execute_script(filename_path, parameters, self.show_cmd)

    def download_log_data(self, data_logger_client, remote_path, remote_log, new_log):
        filename_path = "01_data_collection/download_log_data.sh"
        parameters = [self.ip, self.username, self.password, data_logger_client.ip, data_logger_client.username,
                      data_logger_client.password, remote_path, remote_log, self.path, new_log]
        ScriptHelper.execute_script(filename_path, parameters, self.show_cmd)

    def download_time_file(self, data_logger_client, time_file):
        filename_path = "01_data_collection/download_atop_data.sh"
        parameters = [self.ip, self.username, self.password, data_logger_client.ip, data_logger_client.username,
                      data_logger_client.password, data_logger_client.path, time_file, self.path]
        ScriptHelper.execute_script(filename_path, parameters, self.show_cmd)

    def centralize_data(self, data_logger_client, other_data=False, remote_paths=[], remote_files=[]):
        self.download_atop_data(data_logger_client)
        if other_data:  # download apache continuum's log
            for index, remote_path in enumerate(remote_paths):
                remote_file = remote_files[index]
                new_file = '{0}_{1}'.format(data_logger_client.hostname, remote_file)
                self.download_log_data(data_logger_client, remote_path, remote_file, new_file)

    def centralize_time_files(self, data_logger_client, time_files):
        for time_file in time_files:
            self.download_time_file(data_logger_client, time_file)

    def restart_rsyslog(self):
        filename_path = "04_general/restart_service.sh"
        service_name = "rsyslog"
        parameters = [self.ip, self.username, self.password, service_name]
        ScriptHelper.execute_script(filename_path, parameters, self.show_cmd)

    def refresh_syslog_file(self):
        filename_path = "04_general/refresh_rsyslog.sh"
        service_name = "rsyslog"
        parameters = [self.ip, self.username, self.password, service_name]
        ScriptHelper.execute_script(filename_path, parameters, self.show_cmd)


    def clean_data_collection(self):
        self.restart_rsyslog()

    """

    """


class DataLoggerClient(Machine, implements(IConfigurationCommon), implements(IDataCollection)):
    dls = None  # store information of data logger server

    def __init__(self, hostname, ip, username, password, path, network_interface, tcp_file="traffic.pcap",
                 tcp_pids_file="tcp_pids.txt", atop_interval=1, time_window_traffic=1):
        super().__init__(hostname, ip, username, password, path)
        self.path = path
        self.network_interface = network_interface
        self.tcp_file = tcp_file
        self.tcp_pids_file = tcp_pids_file
        self.atop_interval = atop_interval
        self.time_window_traffic = time_window_traffic

    def configure(self):
        self.configure_base()
        self.configure_data_collection()

    def configure_base(self):
        filename_path = "00_configuration/DataLogger/DataLoggerServer_base.sh"
        parameters = [self.ip, self.username, self.password]
        ScriptHelper.execute_script(filename_path, parameters, self.show_cmd)

    def configure_data_collection(self):
        filename_path = "00_configuration/DataLogger/DataLoggerServer_data_collection.sh"
        parameters = [self.ip, self.username, self.password, self.controller_ip, self.controller_username,
                      self.controller_password, self.controller_path]
        ScriptHelper.execute_script(filename_path, parameters, self.show_cmd)

    def start_collect_data(self):
        filename_path = "01_data_collection/start_packet.sh"
        parameters = [self.ip, self.username, self.password, self.path, self.tcp_file, self.network_interface,
                      self.tcp_pids_file]
        ScriptHelper.execute_script(filename_path, parameters, self.show_cmd)

    def stop_collect_data(self):
        filename_path = "04_general/kill_pids.sh"
        parameters = [self.ip, self.username, self.password, self.path, self.tcp_pids_file]
        ScriptHelper.execute_script(filename_path, parameters, self.show_cmd)

    def download_atop_data(self, data_logger_client):
        filename_path = "01_data_collection/download_atop_data.sh"
        parameters = [self.ip, self.username, self.password, data_logger_client.ip, data_logger_client.username,
                      data_logger_client.password, data_logger_client.path, data_logger_client.atop_file, self.path]
        ScriptHelper.execute_script(filename_path, parameters, self.show_cmd)

    def download_log_data(self, data_logger_client, remote_path, remote_log, new_log):
        filename_path = "01_data_collection/download_log_data.sh"
        parameters = [self.ip, self.username, self.password, data_logger_client.ip, data_logger_client.username,
                      data_logger_client.password, remote_path, remote_log, self.path, new_log]
        ScriptHelper.execute_script(filename_path, parameters, self.show_cmd)

    def download_time_file(self, data_logger_client, time_file):
        filename_path = "01_data_collection/download_atop_data.sh"
        parameters = [self.ip, self.username, self.password, data_logger_client.ip, data_logger_client.username,
                      data_logger_client.password, data_logger_client.path, time_file, self.path]
        ScriptHelper.execute_script(filename_path, parameters, self.show_cmd)

    def centralize_data(self, data_logger_client, other_data=False, remote_paths=[], remote_files=[]):
        self.download_atop_data(data_logger_client)
        if other_data:  # download apache continuum's log
            for index, remote_path in enumerate(remote_paths):
                remote_file = remote_files[index]
                new_file = '{0}_{1}'.format(data_logger_client.hostname, remote_file)
                self.download_log_data(data_logger_client, remote_path, remote_file, new_file)

    def centralize_time_files(self, data_logger_client, time_files):
        for time_file in time_files:
            self.download_time_file(data_logger_client, time_file)

    def restart_rsyslog(self):
        filename_path = "04_general/restart_service.sh"
        service_name = "rsyslog"
        parameters = [self.ip, self.username, self.password, service_name]
        ScriptHelper.execute_script(filename_path, parameters, self.show_cmd)

    def clean_data_collection(self):
        self.restart_rsyslog()


class DataLoggerClient(Machine, implements(IConfigurationCommon), implements(IDataCollection)):
    dls = None  # store information of data logger server

    def __init__(self, hostname, ip, username, password, path, atop_pids_file="atop_pids.txt"):
        super().__init__(hostname, ip, username, password, path)
        self.path = path
        self.atop_file = "{0}.raw".format(hostname)
        self.atop_pids_file = atop_pids_file
        self.atop_interval = str(self.dls.atop_interval)
        self.rsyslog_apache = False  # True will be overridden by Benign and Target Servers

    def configure_base(self):
        filename_path = "00_configuration/DataLogger/DataLoggerClient_base.sh"
        parameters = [self.ip, self.username, self.password]
        ScriptHelper.execute_script(filename_path, parameters, self.show_cmd)

    def configure_data_collection(self):
        if self.rsyslog_apache:
            rsyslog_file = "rsyslog_apache.conf"
        else:
            rsyslog_file = "rsyslog_no_apache.conf"
        filename_path = "00_configuration/DataLogger/DataLoggerClient20_data_collection.sh"
        parameters = [self.ip, self.username, self.password, self.controller_ip, self.controller_username,
                      self.controller_password, self.controller_path, self.dls.ip, rsyslog_file]
        ScriptHelper.execute_script(filename_path, parameters, self.show_cmd)

    def start_collect_data(self):
        filename_path = "01_data_collection/start_atop.sh"
        parameters = [self.ip, self.username, self.password, self.path, self.atop_file, self.atop_interval,
                      self.atop_pids_file, self.controller_ip, self.controller_username, self.controller_password,
                      self.controller_path]
        ScriptHelper.execute_script(filename_path, parameters, self.show_cmd)

    def stop_collect_data(self):
        filename_path = "01_data_collection/stop_atop.sh"
        parameters = [self.ip, self.username, self.password, self.path, self.atop_pids_file]
        ScriptHelper.execute_script(filename_path, parameters, self.show_cmd)


class VulnerableClient(DataLoggerClient, implements(IConfiguration), implements(IConfigurationCommon),
                       implements(IConfigurationAttack), implements(IConfigurationBenign), implements(IDataCollection),
                       implements(IBenignReproduction), implements(ICleaningBenignReproduction)):
    def __init__(self, hostname, ip, username, password, path, server=None, ftp_folder="ftp_folder", sleep_second='2',
                 benign_pids_file="benign_pids.txt"):
        super().__init__(hostname, ip, username, password, path)
        self.server = server  # target server
        self.ftp_folder = ftp_folder
        last_ip = int(ip.split('.')[-1])
        self.virtual_account = "client{0}".format(str(last_ip))
        self.target_virtual_account = "client{0}".format(str(last_ip + 1))
        self.sleep_second = sleep_second
        self.benign_pids_file = benign_pids_file

    def configure(self):
        self.configure_base()
        self.configure_data_collection()
        self.configure_benign_services()
        if Creme.mirai:
            self.configure_mirai()
        if Creme.ransomware:
            self.configure_ransomware()
        if Creme.resource_hijacking:
            self.configure_resource_hijacking()
        if Creme.disk_wipe:
            self.configure_disk_wipe()
        if Creme.end_point_dos:
            self.configure_end_point_dos()
        # if Creme.data_theft:
        #     self.configure_data_theft()
        # if Creme.rootkit_ransomware:
        #     self.configure_rootkit_ransomware()

    def configure_base(self):
        super().configure_base()

    def configure_data_collection(self):
        super().configure_data_collection()

    def configure_benign_services(self):
        filename_path = "00_configuration/Client/Client_benign_services.sh"
        parameters = [self.hostname, self.ip, self.username, self.password, self.path, self.ftp_folder,
                      self.controller_ip, self.controller_username, self.controller_password, self.controller_path,
                      self.server.ip, self.virtual_account, self.server.domain_name]
        ScriptHelper.execute_script(filename_path, parameters, self.show_cmd)

    def start_collect_data(self):
        super().start_collect_data()

    def stop_collect_data(self):
        super().stop_collect_data()

    def configure_mirai(self):
        filename_path = "00_configuration/VulnerableClient/VulnerableClient_mirai.sh"
        parameters = [self.ip, self.username, self.password, self.controller_ip, self.controller_username,
                      self.controller_password, self.controller_path]
        ScriptHelper.execute_script(filename_path, parameters, self.show_cmd)

    def configure_ransomware(self):
        pass

    def configure_resource_hijacking(self):
        pass

    def configure_disk_wipe(self):
        pass

    def configure_end_point_dos(self):
        pass

    # def configure_data_theft(self):
    #     pass
    #
    # def configure_rootkit_ransomware(self):
    #     pass

    def start_benign_behaviors(self):
        filename_path = "00_configuration/Client/Client_start_benign_behaviors.sh"
        parameters = [self.hostname, self.ip, self.username, self.password, self.path, self.ftp_folder,
                      self.target_virtual_account, self.sleep_second, self.benign_pids_file, self.server.domain_name]
        ScriptHelper.execute_script(filename_path, parameters, self.show_cmd)

    def stop_benign_behaviors(self):
        filename_path = "04_general/kill_pids.sh"
        parameters = [self.ip, self.username, self.password, self.path, self.benign_pids_file]
        ScriptHelper.execute_script(filename_path, parameters, self.show_cmd)

    def clean_benign_reproduction(self):
        filename_path = "04_general/kill_pids.sh"
        parameters = [self.ip, self.username, self.password, self.path, self.benign_pids_file]
        ScriptHelper.execute_script(filename_path, parameters, self.show_cmd)

    def tmp_noexec(self):
        filename_path = "00_configuration/VulnerableClient/VulnerableClient_tmp_noexec.sh"
        parameters = [self.ip, self.username, self.password, self.server.ip]
        ScriptHelper.execute_script(filename_path, parameters, self.show_cmd)


class NonVulnerableClient(DataLoggerClient, implements(IConfiguration), implements(IConfigurationCommon),
                          implements(IConfigurationBenign), implements(IDataCollection),
                          implements(IBenignReproduction), implements(ICleaningBenignReproduction)):
    def __init__(self, hostname, ip, username, password, path, server=None, ftp_folder="ftp_folder", sleep_second='2',
                 benign_pids_file="benign_pids.txt"):
        super().__init__(hostname, ip, username, password, path)
        self.server = server  # benign server
        self.ftp_folder = ftp_folder
        last_ip = int(ip.split('.')[-1])
        self.virtual_account = "client{0}".format(str(last_ip))
        self.target_virtual_account = "client{0}".format(str(last_ip + 1))
        self.sleep_second = sleep_second
        self.benign_pids_file = benign_pids_file
        # something else

    def configure(self):
        self.configure_base()
        self.configure_data_collection()
        self.configure_benign_services()

    def configure_base(self):
        super().configure_base()

    def configure_data_collection(self):
        super().configure_data_collection()

    def configure_benign_services(self):
        filename_path = "00_configuration/Client/Client_benign_services.sh"
        parameters = [self.hostname, self.ip, self.username, self.password, self.path, self.ftp_folder,
                      self.controller_ip, self.controller_username, self.controller_password, self.controller_path,
                      self.server.ip, self.virtual_account, self.server.domain_name]
        ScriptHelper.execute_script(filename_path, parameters, self.show_cmd)

    def start_collect_data(self):
        super().start_collect_data()

    def stop_collect_data(self):
        super().stop_collect_data()

    def start_benign_behaviors(self):
        filename_path = "00_configuration/Client/Client_start_benign_behaviors.sh"
        parameters = [self.hostname, self.ip, self.username, self.password, self.path, self.ftp_folder,
                      self.target_virtual_account, self.sleep_second, self.benign_pids_file, self.server.domain_name]
        ScriptHelper.execute_script(filename_path, parameters, self.show_cmd)

    def stop_benign_behaviors(self):
        filename_path = "04_general/kill_pids.sh"
        parameters = [self.ip, self.username, self.password, self.path, self.benign_pids_file]
        ScriptHelper.execute_script(filename_path, parameters, self.show_cmd)

    def clean_benign_reproduction(self):
        filename_path = "04_general/kill_pids.sh"
        parameters = [self.ip, self.username, self.password, self.path, self.benign_pids_file]
        ScriptHelper.execute_script(filename_path, parameters, self.show_cmd)


class TargetServer(DataLoggerClient, implements(IConfiguration), implements(IConfigurationCommon),
                   implements(IConfigurationAttack), implements(IConfigurationBenign), implements(IDataCollection),
                   implements(ICleaningAttackReproduction), implements(ICleaningDataCollection)):
    vulnerable_clients = None
    non_vulnerable_clients = None

    def __init__(self, hostname, ip, username, password, path, domain_name="speedlab.net", attacker_server_ip=""):
        super().__init__(hostname, ip, username, password, path)
        self.rsyslog_apache = True
        self.domain_name = domain_name
        self.attacker_server_ip = attacker_server_ip
        # something else

    def configure(self):
        self.configure_base()
        self.configure_data_collection()
        self.configure_benign_services()
        if Creme.mirai:
            self.configure_mirai()
        if Creme.ransomware:
            self.configure_ransomware()
        if Creme.resource_hijacking:
            self.configure_resource_hijacking()
        if Creme.disk_wipe:
            self.configure_disk_wipe()
        if Creme.end_point_dos:
            self.configure_end_point_dos()
        # if Creme.data_theft:
        #     self.configure_data_theft()
        # if Creme.rootkit_ransomware:
        #     self.configure_rootkit_ransomware()
        self.reboot()
        self.wait_machine_up()

    def configure_base(self):
        super().configure_base()

    def configure_data_collection(self):
        if self.rsyslog_apache:
            rsyslog_file = "rsyslog_apache.conf"
        else:
            rsyslog_file = "rsyslog_no_apache.conf"
        filename_path = "00_configuration/TargetServer/TargetServer_data_collection.sh"
        parameters = [self.ip, self.username, self.password, self.controller_ip, self.controller_username,
                      self.controller_password, self.controller_path, self.dls.ip, rsyslog_file]
        ScriptHelper.execute_script(filename_path, parameters, self.show_cmd)

    def configure_benign_services(self):
        filename_path = "00_configuration/Server/Server_benign_services.sh"
        parameters = [self.hostname, self.ip, self.username, self.password, self.path, self.controller_ip,
                      self.controller_username, self.controller_password, self.controller_path, self.domain_name,
                      self.attacker_server_ip]
        ScriptHelper.execute_script(filename_path, parameters, self.show_cmd)
        # add FTP users
        for client in self.vulnerable_clients:
            filename_path = "00_configuration/Server/Server_create_FTP_user.sh"
            parameters = [self.ip, self.username, self.password, client.hostname, client.password]
            ScriptHelper.execute_script(filename_path, parameters, self.show_cmd)
        for client in self.non_vulnerable_clients:
            filename_path = "00_configuration/Server/Server_create_FTP_user.sh"
            parameters = [self.ip, self.username, self.password, client.hostname, client.password]
            ScriptHelper.execute_script(filename_path, parameters, self.show_cmd)

    def start_collect_data(self):
        super().start_collect_data()

    def stop_collect_data(self):
        super().stop_collect_data()

    def configure_mirai(self):
        pass

    def configure_ransomware(self):
        # ?????
        pass

    def configure_resource_hijacking(self):
        filename_path = "00_configuration/TargetServer/TargetServer_resource_hijacking.sh"
        parameters = [self.ip, self.username, self.password]
        ScriptHelper.execute_script(filename_path, parameters, self.show_cmd)

    def configure_disk_wipe(self):
        # ?????
        pass

    def configure_end_point_dos(self):
        # ?????
        pass

    # to do: use right before running process, think about whether run it during configuration time, but remembering
    # about persistent 00_configuration after reboot
    def configure_end_point_dos_ulimit(self):
        filename_path = "00_configuration/TargetServer/TargetServer_end_point_dos_ulimit.sh"
        parameters = [self.ip, self.username, self.password]
        ScriptHelper.execute_script(filename_path, parameters, self.show_cmd)

    # def configure_data_theft(self):
    #     pass
    #
    # def configure_rootkit_ransomware(self):
    #     pass

    def reboot(self):
        filename_path = "04_general/reboot.sh"
        parameters = [self.ip, self.username, self.password]
        ScriptHelper.execute_script(filename_path, parameters, self.show_cmd)
        time.sleep(90)

    def wait_machine_up(self):
        OtherHelper.wait_machine_up(self.ip)
        # waiting for the machine completely turns on
        time.sleep(180)

    def clean_mirai(self):
        pass

    def clean_disk_wipe(self):
        self.reboot()
        self.wait_machine_up()

    def clean_ransomware(self):
        self.reboot()
        self.wait_machine_up()

    def clean_resource_hijacking(self):
        self.reboot()
        self.wait_machine_up()

    def clean_end_point_dos(self):
        self.reboot()
        self.wait_machine_up()

    # def clean_data_theft(self):
    #     self.reboot()
    #     self.wait_machine_up()
    #
    # def clean_rootkit_ransomware(self):
    #     self.reboot()
    #     self.wait_machine_up()

    def restart_rsyslog(self):
        filename_path = "04_general/restart_service.sh"
        service_name = "rsyslog"
        parameters = [self.ip, self.username, self.password, service_name]
        ScriptHelper.execute_script(filename_path, parameters, self.show_cmd)

    def restart_continuum(self):
        filename_path = "04_general/restart_service.sh"
        service_name = "continuum"
        parameters = [self.ip, self.username, self.password, service_name]
        ScriptHelper.execute_script(filename_path, parameters, self.show_cmd)

    def clean_data_collection(self):
        self.restart_rsyslog()


class BenignServer(DataLoggerClient, implements(IConfiguration), implements(IConfigurationCommon),
                   implements(IConfigurationBenign), implements(IDataCollection), implements(ICleaningDataCollection)):
    vulnerable_clients = None
    non_vulnerable_clients = None

    def __init__(self, hostname, ip, username, password, path, domain_name="speedlab.net", attacker_server_ip=""):
        super().__init__(hostname, ip, username, password, path)
        self.rsyslog_apache = True
        self.domain_name = domain_name
        self.attacker_server_ip = attacker_server_ip
        # something else

    def configure(self):
        self.configure_base()
        self.configure_data_collection()
        self.configure_benign_services()

    def configure_base(self):
        super().configure_base()

    def configure_data_collection(self):
        if self.rsyslog_apache:
            rsyslog_file = "rsyslog_apache.conf"
        else:
            rsyslog_file = "rsyslog_no_apache.conf"
        filename_path = "00_configuration/TargetServer/TargetServer_data_collection.sh"  # similar to target_server
        parameters = [self.ip, self.username, self.password, self.controller_ip, self.controller_username,
                      self.controller_password, self.controller_path, self.dls.ip, rsyslog_file]
        ScriptHelper.execute_script(filename_path, parameters, self.show_cmd)

    def configure_benign_services(self):
        filename_path = "00_configuration/Server/Server_benign_services.sh"
        parameters = [self.hostname, self.ip, self.username, self.password, self.path, self.controller_ip,
                      self.controller_username, self.controller_password, self.controller_path, self.domain_name,
                      self.attacker_server_ip]
        ScriptHelper.execute_script(filename_path, parameters, self.show_cmd)
        # add FTP users
        for client in self.vulnerable_clients:
            filename_path = "00_configuration/Server/Server_create_FTP_user.sh"
            parameters = [self.ip, self.username, self.password, client.hostname, client.password]
            ScriptHelper.execute_script(filename_path, parameters, self.show_cmd)
        for client in self.non_vulnerable_clients:
            filename_path = "00_configuration/Server/Server_create_FTP_user.sh"
            parameters = [self.ip, self.username, self.password, client.hostname, client.password]
            ScriptHelper.execute_script(filename_path, parameters, self.show_cmd)

    def start_collect_data(self):
        super().start_collect_data()

    def stop_collect_data(self):
        super().stop_collect_data()

    def restart_rsyslog(self):
        filename_path = "04_general/restart_service.sh"
        service_name = "rsyslog"
        parameters = [self.ip, self.username, self.password, service_name]
        ScriptHelper.execute_script(filename_path, parameters, self.show_cmd)

    def restart_continuum(self):
        filename_path = "04_general/restart_service.sh"
        service_name = "continuum"
        parameters = [self.ip, self.username, self.password, service_name]
        ScriptHelper.execute_script(filename_path, parameters, self.show_cmd)

    def clean_data_collection(self):
        self.restart_rsyslog()


class AttackerServer(Machine, implements(IConfiguration), implements(IConfigurationCommon),
                     implements(IConfigurationAttack), implements(IMiraiAttackerServer),
                     implements(ICleaningAttackReproduction), implements(IConfigurationAttackerSide),
                     implements(IDiskWipeAttackerServer), implements(IRansomwareAttackerServer),
                     implements(IResourceHijackingAttackerServer), implements(IEndPointDosAttackerServer)):
    data_logger_server_ip = None
    DNS_server_ip = None
    mirai_o4_xxx_1 = None
    mirai_o4_xxx_2 = None

    def __init__(self, hostname, ip, username, password, path="/home/kali/Desktop/reinstall",
                 cnc_pids_file="cnc_pids.txt", transfer_pids_file="transfer_pids.txt", number_of_new_bots="3",
                 targeted_attack="", DDoS_type="udp", DDoS_duration="30"):
        super().__init__(hostname, ip, username, password, path)
        self.cnc_pids_file = cnc_pids_file
        self.transfer_pids_file = transfer_pids_file
        self.bot_input_files = []
        self.num_of_new_bots = number_of_new_bots
        self.targeted_attack = targeted_attack
        self.DDoS_type = DDoS_type
        self.DDoS_duration = DDoS_duration
        self.killed_pids_file = "killed_pids.txt"
        # self.flag_finish = "Creme_finish_attack_scenario"
# configuration block

    def configure(self):
        self.configure_base()
        self.configure_data_collection()
        if Creme.mirai:
            self.configure_mirai()
        # if Creme.ransomware or Creme.resource_hijacking or Creme.disk_wipe or Creme.end_point_dos or \
        #         Creme.data_theft or Creme.rootkit_ransomware:
        if Creme.ransomware or Creme.resource_hijacking or Creme.disk_wipe or Creme.end_point_dos:
            self.configure_pymetasploit()
            self.configure_apache2()
        if Creme.ransomware:
            self.configure_ransomware()
        if Creme.resource_hijacking:
            self.configure_resource_hijacking()
        if Creme.disk_wipe:
            self.configure_disk_wipe()
        if Creme.end_point_dos:
            self.configure_end_point_dos()
        # if Creme.data_theft:
        #     self.configure_data_theft()
        # if Creme.rootkit_ransomware:
        #     self.configure_rootkit_ransomware()

    def configure_base(self):
        filename_path = "00_configuration/AttackerServer/AttackerServer_base.sh"
        parameters = [self.ip, self.username, self.password, self.controller_ip, self.controller_username,
                      self.controller_password, self.controller_path, self.DNS_server_ip]
        ScriptHelper.execute_script(filename_path, parameters, self.show_cmd)

    def configure_data_collection(self):
        filename_path = "00_configuration/AttackerServer/AttackerServer_data_collection.sh"
        parameters = [self.ip, self.username, self.password, self.data_logger_server_ip]
        ScriptHelper.execute_script(filename_path, parameters, self.show_cmd)

    def configure_mirai(self):
        ip_o = self.ip.split(".")
        mirai_dns_xxx = self.DNS_server_ip.replace(".", ",")

        filename_path = "00_configuration/AttackerServer/AttackerServer_mirai.sh"
        parameters = [self.ip, self.username, self.password, self.path, self.controller_ip, self.controller_username,
                      self.controller_password, self.controller_path, self.transfer_pids_file, mirai_dns_xxx,
                      ip_o[0], ip_o[1], ip_o[2], '"' + self.mirai_o4_xxx_1 + '"', '"' + self.mirai_o4_xxx_2 + '"']
        ScriptHelper.execute_script(filename_path, parameters, self.show_cmd)

    def configure_pymetasploit(self):
        filename_path = "00_configuration/AttackerServer/AttackerServer_pymetasploit.sh"
        parameters = [self.ip, self.username, self.password, self.path]
        ScriptHelper.execute_script(filename_path, parameters, self.show_cmd)

    def configure_apache2(self):
        filename_path = "00_configuration/AttackerServer/AttackerServer_apache2.sh"
        parameters = [self.ip, self.username, self.password]
        ScriptHelper.execute_script(filename_path, parameters, self.show_cmd)

    def configure_disk_wipe(self):
        prepared_files = "CREMEv2/CREME_backend_execution/scripts/02_scenario/02_disk_wipe/python_files/attacker_server"
        filename_path = "00_configuration/AttackerServer/AttackerServer_disk_wipe.sh"
        parameters = [self.ip, self.username, self.password, self.path, self.controller_ip, self.controller_username,
                      self.controller_password, self.controller_path, prepared_files]
        ScriptHelper.execute_script(filename_path, parameters, self.show_cmd)

    def configure_ransomware(self):
        prepared_files = "CREMEv2/CREME_backend_execution/scripts/02_scenario/03_ransomware/python_files/attacker_server"
        filename_path = "00_configuration/AttackerServer/AttackerServer_ransomware.sh"
        parameters = [self.ip, self.username, self.password, self.path, self.controller_ip, self.controller_username,
                      self.controller_password, self.controller_path, prepared_files]
        ScriptHelper.execute_script(filename_path, parameters, self.show_cmd)

    def configure_resource_hijacking(self):
        prepared_files = "CREMEv2/CREME_backend_execution/scripts/02_scenario/04_resource_hijacking/python_files/attacker_server"
        filename_path = "00_configuration/AttackerServer/AttackerServer_resource_hijacking.sh"
        parameters = [self.ip, self.username, self.password, self.path, self.controller_ip, self.controller_username,
                      self.controller_password, self.controller_path, prepared_files]
        ScriptHelper.execute_script(filename_path, parameters, self.show_cmd)

    def configure_end_point_dos(self):
        prepared_files = "CREMEv2/CREME_backend_execution/scripts/02_scenario/05_end_point_dos/python_files/attacker_server"
        filename_path = "00_configuration/AttackerServer/AttackerServer_end_point_dos.sh"
        parameters = [self.ip, self.username, self.password, self.path, self.controller_ip, self.controller_username,
                      self.controller_password, self.controller_path, prepared_files]
        ScriptHelper.execute_script(filename_path, parameters, self.show_cmd)

    # def configure_data_theft(self):
    #     prepared_files = "CREME-N/CREME_backend_execution/scripts/02_scenario/07_data_theft/python_files/attacker_server"
    #     filename_path = "00_configuration/AttackerServer/AttackerServer_data_theft.sh"
    #     parameters = [self.ip, self.username, self.password, self.path, self.controller_ip, self.controller_username,
    #                   self.controller_password, self.controller_path, prepared_files]
    #     ScriptHelper.execute_script(filename_path, parameters, self.show_cmd)
    #
    # def configure_rootkit_ransomware(self):
    #     prepared_files = "CREME-N/CREME_backend_execution/scripts/02_scenario/08_rootkit_ransomware/python_files/attacker_server"
    #     filename_path = "00_configuration/AttackerServer/AttackerServer_rootkit_ransomware.sh"
    #     parameters = [self.ip, self.username, self.password, self.path, self.controller_ip, self.controller_username,
    #                   self.controller_password, self.controller_path, prepared_files]
    #     ScriptHelper.execute_script(filename_path, parameters, self.show_cmd)

    # Mirai Attack Block
    def mirai_start_metasploit(self):
        filename_path = "02_scenario/01_mirai/bash_files/00_AttackerServer_start_metasploit_Mirai.sh"
        parameters = [self.ip, self.username, self.password, self.path, self.killed_pids_file]
        ScriptHelper.execute_script(filename_path, parameters, self.show_cmd)

    def mirai_first_step(self):
        filename_path = "02_scenario/01_mirai/bash_files/01_step_mirai_AttackerServer_PRE.sh"
        parameters = [self.ip, self.username, self.password, self.path, self.targeted_attack]
        ScriptHelper.execute_script(filename_path, parameters, self.show_cmd)

    def mirai_second_step(self):
        filename_path = "02_scenario/01_mirai/bash_files/02_step_mirai_AttackerServer_PRE.sh"
        parameters = [self.ip, self.username, self.password, self.path, self.targeted_attack]
        ScriptHelper.execute_script(filename_path, parameters, self.show_cmd)

    # start cnc and login
    def mirai_start_cnc_and_login(self):
        logs_path = "CREME_backend_execution/logs/01_mirai/times"
        outputTime = "time_step_3_mirai_start_cnc_and_login.txt"

        filename_path = "02_scenario/01_mirai/bash_files/03_step_AttackerServer_start_cnc_and_login.sh"
        parameters = [self.hostname, self.ip, self.username, self.password, self.path, self.cnc_pids_file,
                      self.num_of_new_bots, self.targeted_attack, self.DDoS_type, self.DDoS_duration, logs_path, outputTime]
        ScriptHelper.execute_script(filename_path, parameters, self.show_cmd)

    def mirai_wait_for_finish_scan(self):
        logs_path = "CREME_backend_execution/logs/01_mirai/times"
        outputTime = "time_step_6_mirai_wait_finish_scan.txt"

        FinishedFile = "ScanFinishedFile.txt"

        filename_path = "02_scenario/01_mirai/bash_files/06_step_AttackerServer_wait_for_finished_phase.sh"
        parameters = [self.ip, self.username, self.password, self.path, FinishedFile, logs_path, outputTime]
        ScriptHelper.execute_script(filename_path, parameters, self.show_cmd)

    def mirai_transfer_and_start_malicious(self):
        scan_flag = "0"
        input_bot = "input_bot"  # example: input_bot_192.168.1.112.txt
        logs_path = "CREME_backend_execution/logs/01_mirai/times"
        output_time = "time_step_7_start_transfer.txt"

        filename_path = "02_scenario/01_mirai/bash_files/07_step_AttackerServer_transfer_and_start_malicious.sh"
        parameters = [self.ip, self.username, self.password, self.path, input_bot, scan_flag, self.transfer_pids_file,
                      logs_path, output_time]
        ScriptHelper.execute_script(filename_path, parameters, self.show_cmd)

    def mirai_wait_for_finished_transfer(self):
        logs_path = "CREME_backend_execution/logs/01_mirai/times"
        outputTime = "time_step_7_mirai_wait_finish_transfer.txt"

        FinishedFile = "TransferFinishedFile.txt"

        filename_path = "02_scenario/01_mirai/bash_files/06_step_AttackerServer_wait_for_finished_phase.sh"
        parameters = [self.ip, self.username, self.password, self.path, FinishedFile, logs_path, outputTime]
        ScriptHelper.execute_script(filename_path, parameters, self.show_cmd)

    def mirai_wait_for_finished_ddos(self):
        logs_path = "CREME_backend_execution/logs/01_mirai/times"
        outputTime = "time_step_8_mirai_wait_finish_ddos.txt"

        FinishedFile = "ddosFinishedFile.txt"

        filename_path = "02_scenario/01_mirai/bash_files/06_step_AttackerServer_wait_for_finished_phase.sh"
        parameters = [self.ip, self.username, self.password, self.path, FinishedFile, logs_path, outputTime]
        ScriptHelper.execute_script(filename_path, parameters, self.show_cmd)

    def stop_malicious(self):
        logs_path = "CREME_backend_execution/logs/01_mirai/times"
        outputTime = "time_step_8_mirai_stop_malicious.txt"

        filename_path = "02_scenario/01_mirai/bash_files/08_step_AttackerServer_cnc_stop_malicious.sh"
        parameters = [self.ip, self.username, self.password, self.path, self.transfer_pids_file, logs_path, outputTime]
        ScriptHelper.execute_script(filename_path, parameters, self.show_cmd)

    def stop_cnc_and_login(self):
        filename_path = "./kill_pids.sh"
        parameters = [self.ip, self.username, self.password, self.path, self.cnc_pids_file]
        ScriptHelper.execute_script(filename_path, parameters, self.show_cmd)

    def clean_mirai(self):
        self.stop_malicious()
        self.stop_cnc_and_login()

    # Disk Wipe Attack Block
    def disk_wipe_start_metasploit(self):
        filename_path = "02_scenario/02_disk_wipe/bash_files/00_AttackerServer_start_metasploit_DiskWipe.sh"
        parameters = [self.ip, self.username, self.password, self.path, self.killed_pids_file]
        ScriptHelper.execute_script(filename_path, parameters, self.show_cmd)

    def disk_wipe_first_step(self):
        filename_path = "02_scenario/02_disk_wipe/bash_files/01_step_nonmirai_AttackerServer_PRE.sh"
        parameters = [self.ip, self.username, self.password, self.path, self.targeted_attack]
        ScriptHelper.execute_script(filename_path, parameters, self.show_cmd)

    def disk_wipe_second_step(self):
        filename_path = "02_scenario/02_disk_wipe/bash_files/02_step_nonmirai_AttackerServer_PRE.sh"
        parameters = [self.ip, self.username, self.password, self.path, self.targeted_attack]
        ScriptHelper.execute_script(filename_path, parameters, self.show_cmd)

    def disk_wipe_third_step(self):
        filename_path = "02_scenario/02_disk_wipe/bash_files/03_step_AttackerServer_DiskWipe.sh"
        parameters = [self.ip, self.username, self.password, self.path, self.targeted_attack]
        ScriptHelper.execute_script(filename_path, parameters, self.show_cmd)

    def disk_wipe_fourth_step(self):
        filename_path = "02_scenario/02_disk_wipe/bash_files/04_step_AttackerServer_DiskWipe.sh"
        parameters = [self.ip, self.username, self.password, self.path, self.targeted_attack]
        ScriptHelper.execute_script(filename_path, parameters, self.show_cmd)

    def disk_wipe_fifth_step(self):
        filename_path = "02_scenario/02_disk_wipe/bash_files/05_step_AttackerServer_DiskWipe.sh"
        parameters = [self.ip, self.username, self.password, self.path, self.targeted_attack]
        ScriptHelper.execute_script(filename_path, parameters, self.show_cmd)

    def disk_wipe_sixth_step(self):
        filename_path = "02_scenario/02_disk_wipe/bash_files/06_step_AttackerServer_DiskWipe.sh"
        parameters = [self.ip, self.username, self.password, self.path, self.targeted_attack]
        ScriptHelper.execute_script(filename_path, parameters, self.show_cmd)

    # Ransomware Attack Block
    def ransomware_start_metasploit(self):
        filename_path = "02_scenario/03_ransomware/bash_files/00_AttackerServer_start_metasploit_Ransomware.sh"
        parameters = [self.ip, self.username, self.password, self.path, self.killed_pids_file]
        ScriptHelper.execute_script(filename_path, parameters, self.show_cmd)

    def ransomware_first_step(self):
        filename_path = "02_scenario/03_ransomware/bash_files/01_step_nonmirai_AttackerServer_PRE.sh"
        parameters = [self.ip, self.username, self.password, self.path, self.targeted_attack]
        ScriptHelper.execute_script(filename_path, parameters, self.show_cmd)

    def ransomware_second_step(self):
        filename_path = "02_scenario/03_ransomware/bash_files/02_step_nonmirai_AttackerServer_PRE.sh"
        parameters = [self.ip, self.username, self.password, self.path, self.targeted_attack]
        ScriptHelper.execute_script(filename_path, parameters, self.show_cmd)

    def ransomware_third_step(self):
        filename_path = "02_scenario/03_ransomware/bash_files/03_step_AttackerServer_Ransomware.sh"
        parameters = [self.ip, self.username, self.password, self.path, self.targeted_attack]
        ScriptHelper.execute_script(filename_path, parameters, self.show_cmd)

    def ransomware_fourth_step(self):
        filename_path = "02_scenario/03_ransomware/bash_files/04_step_AttackerServer_Ransomware.sh"
        parameters = [self.ip, self.username, self.password, self.path, self.targeted_attack]
        ScriptHelper.execute_script(filename_path, parameters, self.show_cmd)

    def ransomware_fifth_step(self):
        filename_path = "02_scenario/03_ransomware/bash_files/05_step_AttackerServer_Ransomware.sh"
        parameters = [self.ip, self.username, self.password, self.path, self.targeted_attack]
        ScriptHelper.execute_script(filename_path, parameters, self.show_cmd)
    
    def ransomware_sixth_step(self):
        filename_path = "02_scenario/03_ransomware/bash_files/06_step_AttackerServer_Ransomware.sh"
        parameters = [self.ip, self.username, self.password, self.path, self.targeted_attack]
        ScriptHelper.execute_script(filename_path, parameters, self.show_cmd)

    def ransomware_seventh_step(self):
        filename_path = "02_scenario/03_ransomware/bash_files/07_step_AttackerServer_Ransomware.sh"
        parameters = [self.ip, self.username, self.password, self.path, self.targeted_attack]
        ScriptHelper.execute_script(filename_path, parameters, self.show_cmd)

    # Resource Hijacking Attack Block
    def resource_hijacking_start_metasploit(self):
        filename_path = "02_scenario/04_resource_hijacking/bash_files/00_AttackerServer_start_metasploit_ResourceHijacking.sh"
        parameters = [self.ip, self.username, self.password, self.path, self.killed_pids_file]
        ScriptHelper.execute_script(filename_path, parameters, self.show_cmd)

    def resource_hijacking_first_step(self):
        filename_path = "02_scenario/04_resource_hijacking/bash_files/01_step_nonmirai_AttackerServer_PRE.sh"
        parameters = [self.ip, self.username, self.password, self.path, self.targeted_attack]
        ScriptHelper.execute_script(filename_path, parameters, self.show_cmd)

    def resource_hijacking_second_step(self):
        filename_path = "02_scenario/04_resource_hijacking/bash_files/02_step_nonmirai_AttackerServer_PRE.sh"
        parameters = [self.ip, self.username, self.password, self.path, self.targeted_attack]
        ScriptHelper.execute_script(filename_path, parameters, self.show_cmd)

    def resource_hijacking_third_step(self):
        filename_path = "02_scenario/04_resource_hijacking/bash_files/03_step_AttackerServer_ResourceHijacking.sh"
        parameters = [self.ip, self.username, self.password, self.path, self.targeted_attack]
        ScriptHelper.execute_script(filename_path, parameters, self.show_cmd)


    def resource_hijacking_fourth_step(self):
        filename_path = "02_scenario/04_resource_hijacking/bash_files/04_step_AttackerServer_ResourceHijacking.sh"
        parameters = [self.ip, self.username, self.password, self.path, self.targeted_attack]
        ScriptHelper.execute_script(filename_path, parameters, self.show_cmd)

    def resource_hijacking_fifth_step(self):
        filename_path = "02_scenario/04_resource_hijacking/bash_files/05_step_AttackerServer_ResourceHijacking.sh"
        parameters = [self.ip, self.username, self.password, self.path, self.targeted_attack]
        ScriptHelper.execute_script(filename_path, parameters, self.show_cmd)

    def resource_hijacking_sixth_step(self):
        filename_path = "02_scenario/04_resource_hijacking/bash_files/06_step_AttackerServer_ResourceHijacking.sh"
        parameters = [self.ip, self.username, self.password, self.path, self.targeted_attack]
        ScriptHelper.execute_script(filename_path, parameters, self.show_cmd)

    def resource_hijacking_seventh_step(self):
        filename_path = "02_scenario/04_resource_hijacking/bash_files/07_step_AttackerServer_ResourceHijacking.sh"
        parameters = [self.ip, self.username, self.password, self.path, self.targeted_attack]
        ScriptHelper.execute_script(filename_path, parameters, self.show_cmd)

    # End-Point Dos Attack Block
    def end_point_dos_start_metasploit(self):
        filename_path = "02_scenario/05_end_point_dos/bash_files/00_AttackerServer_start_metasploit_EndPointDos.sh"
        parameters = [self.ip, self.username, self.password, self.path, self.killed_pids_file]
        ScriptHelper.execute_script(filename_path, parameters, self.show_cmd)

    def end_point_dos_first_step(self):
        filename_path = "02_scenario/05_end_point_dos/bash_files/01_step_nonmirai_AttackerServer_PRE.sh"
        parameters = [self.ip, self.username, self.password, self.path, self.targeted_attack]
        ScriptHelper.execute_script(filename_path, parameters, self.show_cmd)

    def end_point_dos_second_step(self):
        filename_path = "02_scenario/05_end_point_dos/bash_files/02_step_nonmirai_AttackerServer_PRE.sh"
        parameters = [self.ip, self.username, self.password, self.path, self.targeted_attack]
        ScriptHelper.execute_script(filename_path, parameters, self.show_cmd)

    def end_point_dos_third_step(self):
        filename_path = "02_scenario/05_end_point_dos/bash_files/03_step_AttackerServer_EndPointDos.sh"
        parameters = [self.ip, self.username, self.password, self.path, self.targeted_attack]
        ScriptHelper.execute_script(filename_path, parameters, self.show_cmd)

    def end_point_dos_fourth_step(self):
        filename_path = "02_scenario/05_end_point_dos/bash_files/04_step_AttackerServer_EndPointDos.sh"
        parameters = [self.ip, self.username, self.password, self.path, self.targeted_attack]
        ScriptHelper.execute_script(filename_path, parameters, self.show_cmd)

    def end_point_dos_fifth_step(self):
        filename_path = "02_scenario/05_end_point_dos/bash_files/05_step_AttackerServer_EndPointDos.sh"
        parameters = [self.ip, self.username, self.password, self.path, self.targeted_attack]
        ScriptHelper.execute_script(filename_path, parameters, self.show_cmd)

    def end_point_dos_sixth_step(self):
        new_user_account = "cremetest"
        new_user_password = "password"
        filename_path = "02_scenario/05_end_point_dos/bash_files/06_step_AttackerServer_EndPointDos.sh"
        parameters = [self.ip, self.username, self.password, self.path, self.targeted_attack,
                      new_user_account, new_user_password]
        ScriptHelper.execute_script(filename_path, parameters, self.show_cmd)

    def end_point_dos_seventh_step(self):
        new_user_account = "cremetest"  # must be same as the second stage
        new_user_password = "password"
        filename_path = "02_scenario/05_end_point_dos/bash_files/07_step_AttackerServer_EndPointDos.sh"
        parameters = [self.ip, self.username, self.password, self.path, self.targeted_attack,
                      new_user_account, new_user_password]
        ScriptHelper.execute_script(filename_path, parameters, self.show_cmd)

# ## Data Theft Attack Block
#     def data_theft_start_metasploit(self):
#         filename_path = "02_scenario/07_data_theft/bash_files/00_AttackerServer_start_metasploit_PRE.sh"
#         parameters = [self.ip, self.username, self.password, self.path, self.killed_pids_file]
#         ScriptHelper.execute_script(filename_path, parameters, self.show_cmd)
#
#     def data_theft_first_stage(self):
#         parameters = [self.ip, self.username, self.password, self.path, self.targeted_attack]
#         ScriptHelper.execute_script(filename_path, parameters, self.show_cmd)
#
#     def data_theft_second_stage(self):
#         filename_path = "02_scenario/07_data_theft/bash_files/04_step_AttackerServer_EndPointDos.sh"
#         parameters = [self.ip, self.username, self.password, self.path, self.targeted_attack]
#         ScriptHelper.execute_script(filename_path, parameters, self.show_cmd)
#
#     def data_theft_third_stage(self):
#         filename_path = "02_scenario/07_data_theft/bash_files/05_step_AttackerServer_EndPointDos.sh"
#         parameters = [self.ip, self.username, self.password, self.path, self.targeted_attack]
#         ScriptHelper.execute_script(filename_path, parameters, self.show_cmd)


# ## Rootkit Attack Block
#     def rootkit_ransomware_start_metasploit(self):
#         filename_path = "02_scenario/08_rootkit_ransomware/bash_files/./00_AttackerServer_start_metasploit_PRE.sh"
#         parameters = [self.ip, self.username, self.password, self.path, self.killed_pids_file]
#         ScriptHelper.execute_script(filename_path, parameters, self.show_cmd)
#
#     def rootkit_ransomware_first_stage(self):
#         filename_path = "02_scenario/08_rootkit_ransomware/bash_files/./03_step_AttackerServer_EndPointDos.sh"
#         parameters = [self.ip, self.username, self.password, self.path, self.targeted_attack]
#         ScriptHelper.execute_script(filename_path, parameters, self.show_cmd)
#
#     def rootkit_ransomware_second_stage(self):
#         filename_path = "02_scenario/08_rootkit_ransomware/bash_files/./04_step_AttackerServer_EndPointDos.sh"
#         parameters = [self.ip, self.username, self.password, self.path, self.targeted_attack]
#         ScriptHelper.execute_script(filename_path, parameters, self.show_cmd)
#
#     def rootkit_ransomware_third_stage(self):
#         filename_path = "02_scenario/08_rootkit_ransomware/bash_files/./05_step_AttackerServer_EndPointDos.sh"
#         parameters = [self.ip, self.username, self.password, self.path, self.targeted_attack]
#         ScriptHelper.execute_script(filename_path, parameters, self.show_cmd)

    def stop_metasploit(self):
        filename_path = "./kill_pids.sh"
        parameters = [self.ip, self.username, self.password, self.path, self.killed_pids_file]
        ScriptHelper.execute_script(filename_path, parameters, self.show_cmd)

    def clean_disk_wipe(self):
        self.stop_metasploit()

    def clean_ransomware(self):
        self.stop_metasploit()

    def clean_resource_hijacking(self):
        self.stop_metasploit()

    def clean_end_point_dos(self):
        self.stop_metasploit()

    # def clean_data_theft(self):
    #     self.stop_metasploit()
    #
    # def clean_rootkit_ransomware(self):
    #     self.stop_metasploit()


class MaliciousClient(Machine, implements(IConfiguration), implements(IConfigurationCommon),
                      implements(IConfigurationAttack), implements(IMiraiMaliciousClient),
                      implements(IConfigurationAttackerSide)):
    data_logger_server_ip = None
    attacker_server = None
    DNS_server_ip = None

    def __init__(self, hostname, ip, username, password, path, mirai_pids_file="mirai_pids.txt"):
        super().__init__(hostname, ip, username, password, path)
        self.path = path
        self.mirai_pids_file = mirai_pids_file
        # do something else

    def configure(self):
        self.configure_base()
        self.configure_data_collection()
        if Creme.mirai:
            self.configure_mirai()
        # if Creme.ransomware or Creme.resource_hijacking or Creme.disk_wipe or Creme.end_point_dos or \
        #         Creme.data_theft or Creme.rootkit_ransomware:
        if Creme.ransomware or Creme.resource_hijacking or Creme.disk_wipe or Creme.end_point_dos:
            self.configure_pymetasploit()
            self.configure_apache2()
        if Creme.ransomware:
            self.configure_ransomware()
        if Creme.resource_hijacking:
            self.configure_resource_hijacking()
        if Creme.disk_wipe:
            self.configure_disk_wipe()
        if Creme.end_point_dos:
            self.configure_end_point_dos()
        # if Creme.data_theft:
        #     self.configure_data_theft()
        # if Creme.rootkit_ransomware:
        #     self.configure_rootkit_ransomware()

    def configure_base(self):
        filename_path = "00_configuration/MaliciousClient/MaliciousClient_base.sh"
        parameters = [self.ip, self.username, self.password, self.controller_ip, self.controller_username,
                      self.controller_password, self.controller_path, self.DNS_server_ip]
        ScriptHelper.execute_script(filename_path, parameters, self.show_cmd)

    def configure_data_collection(self):
        filename_path = "00_configuration/MaliciousClient/MaliciousClient_data_collection.sh"
        parameters = [self.ip, self.username, self.password, self.data_logger_server_ip]
        ScriptHelper.execute_script(filename_path, parameters, self.show_cmd)

    def configure_mirai(self):
        filename_path = "00_configuration/MaliciousClient/MaliciousClient_mirai.sh"
        parameters = [self.ip, self.username, self.password, self.path, self.attacker_server.ip,
                      self.attacker_server.username, self.attacker_server.password, self.attacker_server.path]
        ScriptHelper.execute_script(filename_path, parameters, self.show_cmd)

    def configure_pymetasploit(self):
        pass

    def configure_apache2(self):
        pass

    def configure_ransomware(self):
        # ?????
        pass

    def configure_resource_hijacking(self):
        # ?????
        pass

    def configure_disk_wipe(self):
        # ?????
        pass

    def configure_end_point_dos(self):
        # ?????
        pass

    # def configure_data_theft(self):
    #     pass

    # def configure_rootkit_ransomware(self):
    #     pass

    def mirai_start_malicious(self):
        logs_path = "CREME_backend_execution/logs/01_mirai/times"
        outputTime = "time_step_5_kali_start_scan.txt"

        filename_path = "02_scenario/01_mirai/bash_files/05_step_MaliciousClient_start_malicious.sh"
        parameters = [self.ip, self.username, self.password, self.path, self.mirai_pids_file, logs_path, outputTime]
        ScriptHelper.execute_script(filename_path, parameters, self.show_cmd)

    def mirai_stop_malicious(self):
        logs_path = "CREME_backend_execution/logs/01_mirai/times"
        outputTime = "time_step_6_MaliciousClient_stop_malicious.txt"

        filename_path = "02_scenario/01_mirai/bash_files/06_step_MaliciousClient_stop_malicious.sh"
        parameters = [self.ip, self.username, self.password, self.path, self.mirai_pids_file, logs_path, outputTime]
        ScriptHelper.execute_script(filename_path, parameters, self.show_cmd)
