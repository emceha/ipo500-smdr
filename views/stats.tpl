% rebase('header.tpl', title='SMDR / STATS')  
  <div id="container">
    %for table in data:
    <div class="child">
      <table class="main">
      % for n, row in enumerate(table):
        % if n == 0:
          <tr class="header"> 
        % elif n % 2 == 0:
          <tr class="even">
        % else:
          <tr class="odd">
        % end 
        %for m, col in enumerate(row):
          % if n == 0:
            <td class="left">{{col}}<td>
          % else:
            <td class="right">{{col}}<td>
          % end
        %end
          </tr>
      % end
      </table>
    </div>
    % end
  </div>
    