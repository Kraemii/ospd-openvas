# -*- coding: utf-8 -*-
# Copyright (C) 2014-2022 Greenbone Networks GmbH
#
# SPDX-License-Identifier: AGPL-3.0-or-later
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.


from datetime import datetime
from typing import Dict, Union, Any, List, Optional
from uuid import UUID

from .message import Message, MessageType


class ScanHostsMessage(Message):
    message_type: MessageType = MessageType.SCAN_START
    topic = "scanner/scan/cmd/notus"

    scan_id: str
    hosts: Dict[str, str]
    ssh_login: str
    ssh_password: str

    def __init__(
        self,
        *,
        scan_id: str,
        hosts: Dict[str, str],
        ssh_login: str,
        ssh_password: Optional[str] = "",
        ssh_key: Optional[str] = "",
        ssh_port: Optional[int] = 22,
        message_id: Optional[UUID] = None,
        group_id: Optional[str] = None,
        created: Optional[datetime] = None,
    ):
        super().__init__(
            message_id=message_id, group_id=group_id, created=created
        )
        self.scan_id = scan_id
        self.hosts = hosts
        self.ssh_login = ssh_login
        self.ssh_password = ssh_password
        self.ssh_key = ssh_key
        self.ssh_port = ssh_port

    def serialize(self) -> Dict[str, Union[int, str, List[str]]]:
        message = super().serialize()
        message.update(
            {
                "scan_id": self.scan_id,
                "hosts": self.hosts,
                "ssh_login": self.ssh_login,
                "ssh_password": self.ssh_password,
                "ssh_key": self.ssh_key,
                "ssh_port": self.ssh_port,
            }
        )
        return message

    @classmethod
    def _parse(cls, data: Dict[str, Union[int, str]]) -> Dict[str, Any]:
        kwargs = super()._parse(data)

        kwargs.update(
            {
                "scan_id": data.get("scan_id"),
                "hosts": data.get("hosts"),
                "ssh_login": data.get("ssh_login"),
                "ssh_password": data.get("ssh_password"),
                "ssh_key": data.get("ssh_key"),
                "ssh_port": data.get("ssh_port"),
            }
        )
        return kwargs
