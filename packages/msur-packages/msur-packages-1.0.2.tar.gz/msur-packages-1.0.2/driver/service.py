#!/usr/bin/env python
from loguru import logger
from anyio import create_unix_listener
import socket
import json
import msur_packages.driver.protocol as p
"""
Сервис поддерживает связь с аппаратом, принимает телеметрию, отправляет актуальные управляющие воздействия на аппарат с
частотой 10 Hz
"""


# Сокеты для обмена клиента и сервиса
SERVER_SOCKET = '/tmp/msur-server'
CLIENT_SOCKET = '/tmp/msur-client'


class NotConnected(Exception):
    pass


class Client:
    """
    Клиент для общения с этим сервисом, используются unix сокеты
    """
    def __init__(self):
        self.server_socket_path = SERVER_SOCKET
        self.client_socket_path = CLIENT_SOCKET

    def _send(self, data: bytes):
        with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as s:
            try:
                s.connect(self.server_socket_path)
            except ConnectionRefusedError:
                logger.error('Сервис не запущен!')
                raise NotConnected('Сервис не запущен')
            s.sendall(data)
            data = s.recv(1024)
        return data

    def telemetry(self, timeout=1) -> p.Telemetry:
        """
        Получение телеметрии с аппарата, команда блокирующая, может вызвать исключение ReadTimeout
        :return:
        """
        data = (json.dumps({'command': 0}) + '|').encode()
        raw = self._send(data)
        response = json.loads(raw.decode())
        if 'error' in response:
            raise ConnectionError(response['error'])
        return p.Telemetry(**json.loads(response['result']))

    def send(self):
        data = (json.dumps({'command': 1, 'data': {i.__class__.__name__: i.json() for i in packet}}) + '|').encode()
        self._send(data)


protocol_map = {i.__name__: i for i in [p.XThrust, p.YThrust, p.ZThrust, p.Depth, p.AltSet, p.Yaw, p.XVelocity,
    p.YVelocity, p.PidStats, p.ExternalDevices, p.NavFlag]}


class Service:
    """
    Сервис для взаимодействия с аппаратом
    """
    def __init__(self, auv: p.Service):
        self.service_socket = SERVER_SOCKET
        self.client_socket = CLIENT_SOCKET
        # объект аппарата
        self.auv: p.Service = auv
        self.socket = None

    async def _commands_processing(self, commands) -> bytes:
        # Преобразуем полученные данные в json
        commands = commands.decode().split('|')
        response = []
        for command in commands:
            if command == '':
                continue
            try:
                command = json.loads(command)
            except json.JSONDecodeError:
                logger.error('Ошибка декодирования: {}', command)
                continue
            # Команда запроса телеметрии
            if command['command'] == 0:
                telemetry = self.auv.telemetry
                if telemetry is None:
                    # data = json.dumps({'error': 'Нет подключения к аппарату'}).encode()
                    response.append({'command': 0, 'error': 'Нет подключения к аппарату'})
                else:
                    # data = json.dumps({'result': telemetry.json()}).encode()
                    response.append({'command': 0, 'result': telemetry.json()})
                # Отправляем ответ
            # Команда отправки данных на AUV
            elif command['command'] == 1:
                # Пакет с данными необходимыми для отправки на аппарат, {XThrust: {value: 100}}
                package = command['data']
                # Преобразуем данные
                package = [protocol_map[k](**json.loads(v)) for k, v in package.items()]
                # Отправляем данные на AUV
                await self.auv.send(package)
                response.append({'command': 1, 'result': True})
            else:
                response.append({'command': None, 'result': False})
        return '|'.join([json.dumps(i) for i in response]).encode()

    async def receive_command(self, client):
        # команд всего 2: 0 - получить телеметрию, 1 - отправить данные
        # {command_id: 0, data: []}
        async with client:
            commands = await client.receive(1024)
            data = await self._commands_processing(commands)
            await client.send(data)

    async def run(self):
        listener = await create_unix_listener(self.service_socket)
        await listener.serve(self.receive_command)
