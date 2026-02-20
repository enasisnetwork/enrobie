"""
Operation recipes for managing the projects and execution environment.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.

This file is present within multiple projects, simplifying dependency.
"""



from argparse import ArgumentParser
from io import BytesIO
from sys import argv as sys_argv
from typing import Optional

from encommon.times import Time
from encommon.types import DictStrAny
from encommon.types import strplwr

from wand.color import Color  # type: ignore
from wand.image import Image  # type: ignore

from weasyprint import HTML  # type: ignore



STAMP = '%m/%d/%Y'

SUCCESS = ['success', 'passing']
FAILURE = ['failure', 'failing']



STYLES = (
    """
    :root {

      --background: 9, 9, 9;             /* 090909 */
      --foreground: 249, 249, 249;       /* f9f9f9 */

      --color-gray: 139, 139, 139;       /* 8b8b8b */
      --color-red: 255, 102, 102;        /* ff6666 */
      --color-yellow: 255, 255, 102;     /* ffff66 */
      --color-green: 102, 255, 102;      /* 66ff66 */
      --color-pink: 255, 0, 204;         /* ff00cc */
      --color-teal: 102, 255, 255;       /* 66ffff */
      --color-blue: 102, 204, 255; }     /* 66ccff */


    * {
      border-collapse: collapse;
      border-spacing: 0px;
      border-width: 0px 0px 0px 0px;
      box-sizing: border-box;
      color: rgba(var(--foreground), 1);
      font-family: 'sans-serif';
      font-size: 4px;
      font-style: normal;
      font-weight: 400;
      letter-spacing: 0.10px;
      line-height: 5px;
      list-style-type: none;
      margin: 0px 0px 0px 0px;
      outline: none !important;
      padding: 0px 0px 0px 0px;
      page-break-after: avoid;
      page-break-before: avoid;
      page-break-inside: avoid;
      text-align: left;
      text-decoration: none;
      vertical-align: middle;
      white-space: nowrap; }


    table {
      background-color: rgba(var(--background), 1); }

    table:not(:first-of-type) {
      margin-top: 1px; }


    table>tbody>tr>td {
      border-width: 0.1px 0.1px 0.1px 0.1px;
      border-style: solid;
      padding: 0.5px 2px 1px 2px;
      vertical-align: middle; }


    table>tbody>tr>td.label {
      background-color: rgba(var(--color-gray), 0.5);
      border-right-width: 0px;
      border-color: rgba(var(--color-gray), 1);
      padding-right: 2.5px; }

    table>tbody>tr>td.value {
      font-family: 'monospace'; }

    table>tbody>tr>td.count {
      background-color: rgba(var(--color-gray), 0.25);
      border-color: rgba(var(--color-gray), 1);
      border-left-width: 0px;
      color: rgba(var(--foreground), 0.60);
      font-family: 'monospace'; }

    table>tbody>tr>td.count:empty {
      display: none; }

    table>tbody>tr>td.stamp {
      background-color: rgba(var(--color-gray), 0.25);
      border-left-width: 0px;
      border-color: rgba(var(--color-gray), 1);
      color: rgba(var(--foreground), 0.60);
      font-family: 'monospace'; }


    table.gray>tbody>tr>td.value {
      border-color: rgba(var(--foreground), 1);
      background-color: rgba(var(--foreground), 0.4); }

    table.red>tbody>tr>td.value {
      border-color: rgba(var(--color-red), 1);
      background-color: rgba(var(--color-red), 0.4); }

    table.yellow>tbody>tr>td.value {
      border-color: rgba(var(--color-yellow), 1);
      background-color: rgba(var(--color-yellow), 0.4); }

    table.green>tbody>tr>td.value {
      border-color: rgba(var(--color-green), 1);
      background-color: rgba(var(--color-green), 0.4); }

    table.pink>tbody>tr>td.value {
      border-color: rgba(var(--color-pink), 1);
      background-color: rgba(var(--color-pink), 0.4); }

    table.teal>tbody>tr>td.value {
      border-color: rgba(var(--color-teal), 1);
      background-color: rgba(var(--color-teal), 0.4); }

    table.blue>tbody>tr>td.value {
      border-color: rgba(var(--color-blue), 1);
      background-color: rgba(var(--color-blue), 0.4); }
    """)



def arguments(
    args: Optional[list[str]] = None,
) -> DictStrAny:
    """
    Construct arguments which are associated with the file.

    :param args: Override the source for the main arguments.
    :returns: Construct arguments from command line options.
    """

    parser = ArgumentParser()

    args = args or sys_argv[1:]


    parser.add_argument(
        '--file',
        required=True,
        help=(
            'complete or relative '
            'path to output file'))

    parser.add_argument(
        '--label',
        required=True,
        help=(
            'friendly name for '
            'first badge cell'))

    parser.add_argument(
        '--value',
        required=True,
        help=(
            'actual value for '
            'second badge cell'))

    parser.add_argument(
        '--count',
        help=(
            'optional count for '
            'third badge cell'))

    parser.add_argument(
        '--color',
        choices=[
            'gray',
            'red',
            'yellow',
            'green',
            'pink',
            'teal',
            'blue'],
        help=(
            'color for the value '
            'else automatic'))

    parser.add_argument(
        '--date',
        help=(
            'date for the value '
            'else automatic'))


    return vars(
        parser
        .parse_args(args))



def execution(
    # NOCVR
    args: Optional[list[str]] = None,
) -> None:
    """
    Perform whatever operation is associated with the file.

    :param args: Override the source for the main arguments.
    """

    pargs = arguments(args)

    file = pargs['file']
    label = pargs['label']
    value = pargs['value']
    count = pargs['count']
    color = pargs['color']
    count = pargs['count']


    _value = strplwr(value)

    if _value == 'unknown%':
        _value = 'unknown'


    _count = (
        ''
        if count is None
        else count)


    _color = (
        'gray'
        if color is None
        else color)

    if color is None:

        if _value[-1] == '%':

            eulav = int(
                float(_value[:-1]))

            if eulav == 100:
                _color = 'green'

            elif eulav >= 80:
                _color = 'yellow'

            elif eulav >= 0:
                _color = 'red'

            _value = f'{eulav}%'

        if _value in SUCCESS:
            _color = 'green'

        if _value in FAILURE:
            _color = 'red'


    stamp = (
        Time(pargs['date'])
        .stamp(STAMP))


    badge = (
        f"""
        <style>
        {STYLES}
        </style>
        <table class="{_color}">
          <tbody>
            <tr>
              <td class="label">{label}</td>
              <td class="value">{_value}</td>
              <td class="count">{_count}</td>
              <td class="stamp">{stamp}</td>
            </tr>
          </tbody>
        </table>
        """)


    source = BytesIO()

    (HTML(string=badge)
     .write_pdf(source))

    source.seek(0)

    origin = Image(
        file=source,
        resolution=300)

    with origin as image:

        image.trim(
            Color('transparent'))

        image.format = 'png'

        image.save(filename=file)



if __name__ == '__main__':
    execution()
