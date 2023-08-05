from anyio import create_udp_socket, create_connected_udp_socket
from pydantic import BaseModel, validator
import struct
from abc import ABC, abstractmethod
from msur_packages.crc16 import crc16
from loguru import logger
import anyio


package_telemetry = struct.Struct('!BBffffffffffffBBBBf')
package_control = struct.Struct('!BBbbbbfffffBBBffB')
package_pid = struct.Struct('!BBfff')
package_reboot = struct.Struct('!BBBBBBBB')
package_crc = struct.Struct('!H')

telemetry_keys = [
    '0', 'id', 'roll', 'pitch', 'yaw', 'gyro_z', 'depth', 'altitude', 'velocity_x', 'velocity_y', 'pos_x', 'pos_y',
    'voltage', 'current', 'pid_stat', 'devices_stat', 'leak', 'device_error', 'temperature'
]


class IBase(ABC, BaseModel):

    @abstractmethod
    def encode(self, packet: list) -> list:
        pass

    @staticmethod
    @abstractmethod
    def get_package() -> struct.Struct:
        pass


class PidStats(IBase):
    """
    Класс описывает пакет телеметрии о состоянии ПИД регуляторов
    """
    roll: bool
    pitch: bool
    yaw: bool
    depth: bool
    altitude: bool
    speed_x: bool
    speed_y: bool

    def encode(self, packet: list) -> list:
        value = int(''.join([str(int(i)) for i in reversed(
            [self.roll, self.pitch, self.depth, self.altitude, self.yaw, self.speed_x, self.speed_y, 0])]), 2)
        packet[11] = value
        return packet

    @staticmethod
    def get_package() -> struct.Struct:
        return package_control


class PidConfig(IBase):
    """
    Класс описывает состояние ПИД регулятора
    """
    p: float
    i: float
    d: float

    def encode(self, packet: list) -> list:
        packet[2] = self.p
        packet[4] = self.i
        packet[3] = self.d
        return packet

    @staticmethod
    def get_package() -> struct.Struct:
        return package_pid




class DepthPidConfig(PidConfig):
    """
    Класс описывает состояние ПИД регулятора глубины
    """
    pass


class AltitudePidConfig(PidConfig):
    """
    Класс описывает состояние ПИД регулятора высоты
    """
    pass


class RollPidConfig(PidConfig):
    """
    Класс описывает состояние ПИД регулятора крена
    """
    pass


class PitchPidConfig(PidConfig):
    """
    Класс описывает состояние ПИД регулятора деферента
    """
    pass


class YawPidConfig(PidConfig):
    """
    Класс описывает состояние ПИД регулятора рысканья
    """
    pass


class VelXPidConfig(PidConfig):
    """
    Класс описывает состояние ПИД регулятора скорости по оси X
    """
    pass


class VelYPidConfig(PidConfig):
    """
    Класс описывает состояние ПИД регулятора скорости по оси Y
    """
    pass


class GyroPidConfig(PidConfig):
    pass


class WriteConfig(IBase):
    pid: bool

    def encode(self, packet: list) -> list:
        packet[5] = int(self.pid)
        return packet

    @staticmethod
    def get_package() -> struct.Struct:
        return package_reboot


class RebootConfig(IBase):
    stm: bool = False
    pc: bool = False
    hydro: bool = False

    def encode(self, packet: list) -> list:
        packet[2] = int(self.stm)
        packet[3] = int(self.pc)
        packet[4] = int(self.hydro)
        return packet

    @staticmethod
    def get_package() -> struct.Struct:
        return package_reboot


class ExternalDevices(IBase):
    em_1: bool = False
    em_2: bool = False

    def encode(self, packet: list) -> list:
        value = int(''.join([str(int(i)) for i in reversed([self.em_1, self.em_2, 0, 0, 0, 0, 0, 0])]), 2)
        packet[12] = value
        return packet

    @staticmethod
    def get_package() -> struct.Struct:
        return package_control


class Thrust(IBase):
    value: int

    @validator('value', pre=True)
    def validate_value(cls, v_):
        if v_ > 100:
            return 100
        elif v_ < -100:
            return -100
        return v_

    def encode(self, packet: list) -> list:
        return packet

    @staticmethod
    def get_package() -> struct.Struct:
        return package_control


class FloatValue(IBase):
    value: float

    def encode(self, packet: list) -> list:
        return packet

    @staticmethod
    def get_package() -> struct.Struct:
        return package_control


class XThrust(Thrust):
    def encode(self, packet: list) -> list:
        packet[2] = self.value
        return packet


class YThrust(Thrust):
    def encode(self, packet: list) -> list:
        packet[3] = self.value
        return packet


class WThrust(Thrust):
    def encode(self, packet: list) -> list:
        packet[4] = self.value
        return packet


class ZThrust(Thrust):
    def encode(self, packet: list) -> list:
        packet[5] = self.value
        return packet


class Depth(FloatValue):
    def encode(self, packet: list) -> list:
        packet[6] = self.value
        return packet


class AltSet(FloatValue):
    def encode(self, packet: list) -> list:
        packet[7] = self.value
        return packet


class Yaw(FloatValue):
    def encode(self, packet: list) -> list:
        packet[8] = self.value
        return packet


class XVelocity(FloatValue):
    def encode(self, packet: list) -> list:
        packet[9] = self.value
        return packet


class YVelocity(FloatValue):
    def encode(self, packet: list) -> list:
        packet[10] = self.value
        return packet


class NavFlag(BaseModel):
    value: bool

    @staticmethod
    def get_package() -> struct.Struct:
        return package_control

    def encode(self, packet: list) -> list:
        packet[13] = int(self.value)
        return packet


class LeakStatus(BaseModel):
    main: bool
    imu: bool


class DevicesError(BaseModel):
    pressure_sensor: bool
    imu: bool


class Telemetry(BaseModel):
    roll: float
    pitch: float
    yaw: float
    gyro_z: float
    depth: float
    altitude: float
    velocity_x: float
    velocity_y: float
    pos_x: float
    pos_y: float
    voltage: float
    current: float
    pid_stat: PidStats
    devices_stat: ExternalDevices
    leak: LeakStatus
    device_error: DevicesError
    temperature: float

    @validator('pid_stat', pre=True)
    def validate_pid_stat(cls, v_):
        logger.debug(v_)
        if isinstance(v_, PidStats):
            return v_
        elif isinstance(v_, dict):
            return PidStats(**v_)
        b = '{0:08b}'.format(v_)
        return PidStats(roll=bool(int(b[-1])), pitch=bool(int(b[-2])), yaw=bool(int(b[-5])), depth=bool(int(b[-3])),
                        altitude=bool(int(b[-4])), speed_x=bool(int(b[-6])), speed_y=bool(int(b[-7])))

    @validator('devices_stat', pre=True)
    def validate_devices_stat(cls, v_):
        if isinstance(v_, ExternalDevices):
            return v_
        elif isinstance(v_, dict):
            return ExternalDevices(**v_)
        b = '{0:08b}'.format(v_)
        return ExternalDevices(em_1=bool(int(b[-1])), em_2=bool(int(b[-2])))

    @validator('leak', pre=True)
    def validate_leak(cls, v_):
        if isinstance(v_, LeakStatus):
            return v_
        elif isinstance(v_, dict):
            return LeakStatus(**v_)
        b = '{0:08b}'.format(v_)
        return LeakStatus(main=bool(int(b[-1])), imu=bool(int(b[-2])))

    @validator('device_error', pre=True)
    def validate_device_error(cls, v_):
        if isinstance(v_, DevicesError):
            return v_
        elif isinstance(v_, dict):
            return DevicesError(**v_)
        b = '{0:08b}'.format(v_)
        return DevicesError(pressure_sensor=bool(int(b[-1])), imu=bool(int(b[-2])))

    def get_vector(self, vector):
        return vector(x=self.pitch, y=self.yaw, z=self.roll)


class Service:
    """
    Класс предоставляет клиент для общения с AUV, хранит состояние аппарата
    """
    def __init__(self, auv_address, auv_port, service_port, service_address):
        self.auv_address = auv_address
        self.auv_port = auv_port
        self.service_port = service_port
        self.service_address = service_address
        self.auv = {XThrust.__name__: XThrust(value=0)}
        self.buffer = []
        self.socket = None
        self.counter = 0
        self.connected = False
        self.telemetry = None

    def prepare_package(self, package):
        if len(package) == 0:
            return []
        # получаем вид первого пакета
        structure = package[0].get_package()
        # сортируем все пакеты имеющие другой вид
        not_condition = [i for i in package if i.get_package() is not structure]
        # сортируем все пакеты этого-же вида
        to_send = [i for i in package if i.get_package() is structure]
        # если это пакет управления, то обновляем локальное состояние аппарата и добавляем сохраненные состояния
        if structure is package_control:
            for i in to_send:
                self.auv[i.__class__.__name__] = i
            to_send = [self.auv[i] for i in self.auv]
        return to_send, not_condition, structure

    async def send(self, package):
        """
        :param package:
        :return:
        """
        self.buffer.extend(package)

    message_map = {
        (230, 15): [XThrust, YThrust, ZThrust, Depth, AltSet, Yaw, XVelocity, YVelocity, PidStats, ExternalDevices,
                    NavFlag],
        (110, 3): [DepthPidConfig],
        (111, 3): [AltitudePidConfig],
        (112, 3): [RollPidConfig],
        (113, 3): [PitchPidConfig],
        (114, 3): [YawPidConfig],
        (115, 3): [VelXPidConfig],
        (116, 3): [VelYPidConfig],
        (117, 3): [GyroPidConfig],
        (133, 6): [RebootConfig, WriteConfig],
    }

    @staticmethod
    def get_id(package) -> int:
        return {
            'XThrust': 230, 'YThrust': 230, 'ZThrust': 230, 'AltSet': 230, 'Yaw': 230, 'XVelocity': 230,
            'YVelocity': 230, 'PidStats': 230, 'ExternalDevices': 230, 'NavFlag': 230, 'DepthPidConfig': 110,
            'AltitudePidConfig': 111, 'RollPidConfig': 112, 'PitchPidConfig': 113, 'YawPidConfig': 114,
            'VelXPidConfig': 115, 'VelYPidConfig': 116, 'GyroPidConfig': 117, 'RebootConfig': 133, 'WriteConfig': 133
        }[package[0].__class__.__name__]

    async def run_listener(self):
        async with await create_udp_socket(local_host=self.service_address, local_port=self.service_port) as udp:
            logger.debug('Создан UDP сокет на порту {port}', port=self.service_port)
            async for packet, (host, port) in udp:
                if len(packet) < 2:
                    continue
                crc = package_crc.unpack(packet[-2:])[0]
                if crc != crc16(packet[:-2]):
                    continue
                telemetry = package_telemetry.unpack(packet[:-2])
                dict_ = dict(zip(telemetry_keys, telemetry))
                self.telemetry = Telemetry(**dict_)
                self.connected = True

    async def run_sender(self):
        notification_status = 0
        while True:
            # проверки
            await anyio.sleep(0.1)
            if notification_status == 0:
                logger.info('Нет подключения к аппарату')
                notification_status = 1
            if not self.connected:
                continue
            if notification_status == 1:
                logger.info('Установлено подключение к аппарату')
                notification_status = 2
            # после получения телеметрии создаем сокет для отправки данных
            if self.socket is None:
                self.socket = await create_connected_udp_socket(remote_host=self.auv_address, remote_port=self.auv_port)
                logger.debug('Создаем сокет для отправки')

            # отправляем сообщения на аппарат
            if len(self.buffer) > 0:
                to_send, not_condition, structure = self.prepare_package(self.buffer)
                self.buffer = not_condition[:]
            else:
                to_send, _, structure = self.prepare_package(list(self.auv.values()))

            id_ = self.get_id(to_send)
            buffer = [0, id_, *[0] * {package_control: 15, package_pid: 3, package_reboot: 6}[structure]]
            for i in to_send:
                i.encode(buffer)
            encoded_package = structure.pack(*buffer)

            crc = package_crc.pack(crc16(encoded_package))
            crc_package = encoded_package + crc

            if self.socket is not None:
                await self.socket.send(crc_package)
                self.counter += 1
            else:
                if notification_status == 2:
                    logger.warning('Сокет не доступен для отправки')
                    notification_status = 3
