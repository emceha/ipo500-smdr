% rebase('header.tpl', title='SMDR / IPO500') 
  <div class="table">
    <table class="menu">
      % for n, (path, log) in enumerate(data):
        % if n % 2:
          <tr class="even">
        % else:
          <tr class="odd">
        % end
            <td class="center"> {{n+1}} </td>
            <td class="center"> {{log}} </td>
            <td class="center"><a href="/calls/{{path}}"> Calls </a></td>
            <td class="center"><a href="/stats/int/{{path}}"> Internal </a></td>
            <td class="center"><a href="/stats/ext/{{path}}"> External </a></td>
            <td class="center"><a href="/dsp/log/smdr.log"> ... </a></td>
          </tr>
      % end
    </table>
  </div>