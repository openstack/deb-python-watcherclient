# -*- coding: utf-8 -*-
#
# Copyright 2013 Red Hat, Inc.
# All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from openstackclient.common import utils

from watcherclient._i18n import _
from watcherclient.common import command
from watcherclient.common import utils as common_utils
from watcherclient import exceptions
from watcherclient.v1 import resource_fields as res_fields


class ShowGoal(command.ShowOne):
    """Show detailed information about a given goal."""

    def get_parser(self, prog_name):
        parser = super(ShowGoal, self).get_parser(prog_name)
        parser.add_argument(
            'goal',
            metavar='<goal>',
            help=_('UUID or name of the goal'),
        )
        return parser

    def take_action(self, parsed_args):
        client = getattr(self.app.client_manager, "infra-optim")

        try:
            goal = client.goal.get(parsed_args.goal)
        except exceptions.HTTPNotFound as exc:
            raise exceptions.CommandError(str(exc))

        columns = res_fields.GOAL_FIELDS
        column_headers = res_fields.GOAL_FIELD_LABELS

        return column_headers, utils.get_item_properties(goal, columns)


class ListGoal(command.Lister):
    """List information on retrieved goals."""

    def get_parser(self, prog_name):
        parser = super(ListGoal, self).get_parser(prog_name)
        parser.add_argument(
            '--detail',
            dest='detail',
            action='store_true',
            default=False,
            help=_("Show detailed information about metric collectors."))
        parser.add_argument(
            '--limit',
            metavar='<limit>',
            type=int,
            help=_('Maximum number of goals to return per request, '
                   '0 for no limit. Default is the maximum number used '
                   'by the Watcher API Service.'))
        parser.add_argument(
            '--sort-key',
            metavar='<field>',
            help=_('Goal field that will be used for sorting.'))
        parser.add_argument(
            '--sort-dir',
            metavar='<direction>',
            choices=['asc', 'desc'],
            help=_('Sort direction: "asc" (the default) or "desc".'))

        return parser

    def take_action(self, parsed_args):
        client = getattr(self.app.client_manager, "infra-optim")

        if parsed_args.detail:
            fields = res_fields.GOAL_FIELDS
            field_labels = res_fields.GOAL_FIELD_LABELS
        else:
            fields = res_fields.GOAL_SHORT_LIST_FIELDS
            field_labels = res_fields.GOAL_SHORT_LIST_FIELD_LABELS

        params = {}
        params.update(
            common_utils.common_params_for_list(
                parsed_args, fields, field_labels))

        try:
            data = client.goal.list(**params)
        except exceptions.HTTPNotFound as ex:
            raise exceptions.CommandError(str(ex))

        return (field_labels,
                (utils.get_item_properties(item, fields) for item in data))
