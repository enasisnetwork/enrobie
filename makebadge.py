"""
Operation recipes for managing the projects and execution environment.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.

This file is present within multiple projects, simplifying dependency.
"""



from io import BytesIO
from sys import argv

from encommon.times import Time

from wand.color import Color  # type: ignore
from wand.image import Image  # type: ignore

from weasyprint import HTML  # type: ignore



STYLES = (
    """
    :root {

      --background: 0, 0, 0;             /* 000000 */
      --foreground: 250, 250, 250;       /* fafafa */

      --color-gray: 136, 136, 136;       /* 888888 */
      --color-red: 255, 102, 102;        /* ff6666 */
      --color-pink: 255, 0, 204;         /* ff00cc */
      --color-teal: 102, 255, 255;       /* 66ffff */
      --color-blue: 8, 155, 216;         /* 089bd8 */
      --color-green: 102, 255, 102;      /* 66ff66 */
      --color-yellow: 255, 255, 102;  }  /* ffff66 */


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


    table>tbody>tr>td:nth-child(1) {
      border-right-width: 0px;
      border-color: rgba(var(--color-gray), 1);
      background-color: rgba(var(--color-gray), 0.5);
      padding-right: 2.5px; }

    table>tbody>tr>td:nth-child(2) {
      font-family: 'monospace'; }

    table>tbody>tr>td:nth-child(3) {
      border-left-width: 0px;
      border-color: rgba(var(--color-gray), 1);
      background-color: rgba(var(--color-gray), 0.25);
      color: rgba(var(--foreground), 0.60);
      padding-left: 2.5px; }


    table.gray>tbody>tr>td:nth-child(2) {
      border-color: rgba(var(--foreground), 1);
      background-color: rgba(var(--foreground), 0.4); }

    table.red>tbody>tr>td:nth-child(2) {
      border-color: rgba(var(--color-red), 1);
      background-color: rgba(var(--color-red), 0.4); }

    table.yellow>tbody>tr>td:nth-child(2) {
      border-color: rgba(var(--color-yellow), 1);
      background-color: rgba(var(--color-yellow), 0.4); }

    table.green>tbody>tr>td:nth-child(2) {
      border-color: rgba(var(--color-green), 1);
      background-color: rgba(var(--color-green), 0.4); }

    table.blue>tbody>tr>td:nth-child(2) {
      border-color: rgba(var(--color-blue), 1);
      background-color: rgba(var(--color-blue), 0.4); }

    table.pink>tbody>tr>td:nth-child(2) {
      border-color: rgba(var(--color-pink), 1);
      background-color: rgba(var(--color-pink), 0.4); }

    table.teal>tbody>tr>td:nth-child(2) {
      border-color: rgba(var(--color-teal), 1);
      background-color: rgba(var(--color-teal), 0.4); }
    """)  # noqa: LIT003



CURRENT = (
    (Time(argv[5])
     if len(argv) > 5
     else Time())
    .stamp('%Y-%m-%d'))


BADGE = (
    f"""
    <style>
    {STYLES}
    </style>
    <table class="{argv[3]}">
      <tbody>
        <tr>
          <td>{argv[2]}</td>
          <td>{argv[4]}</td>
          <td>{CURRENT}</td>
        </tr>
      </tbody>
    </table>
    """)



if __name__ == '__main__':


    SOURCE = BytesIO()

    (HTML(string=BADGE)
     .write_pdf(SOURCE))

    SOURCE.seek(0)


    ORIGIN = Image(
        file=SOURCE,
        resolution=300)

    with ORIGIN as IMAGE:

        IMAGE.trim(
            Color('transparent'))

        IMAGE.format = 'png'

        IMAGE.save(
            filename=argv[1])
