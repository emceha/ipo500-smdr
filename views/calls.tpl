% rebase('header.tpl', title='SMDR / CALLS') 
  <div class="table">
    <table class="main">
      % for n, row in enumerate(data):
        % if n == 0:
          <tr class="header">
            <td/>
        % elif n % 2 == 0:
          <tr class="even">
            <td class="right">{{n}}.</td>
        % else:
          <tr class="odd">
            <td class="right">{{n}}.</td> 
        % end
        % for m, col in enumerate(row):
          % if m in [4, 7, 8, 10]:
            <td class="center">{{col}}</td>
          % elif m in [2, 3, 5, 6]:
            <td class="right">{{col}}</td>
          % else:
            <td class="left">{{col}}</td>
          % end
        % end
         </tr>
      % end
    </table>
  </div>