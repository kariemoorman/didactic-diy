<h2 align='center'>SQL</h2>
<h4 align='center'>Database Management: Store, manipulate & retrieve data in databases.</h4>

---

## Table of Contents
- <b>[SQL Data Structures](#overview-of-sql-data-structures)</b>
- <b>[DQL](#dql)</b>
  - <b>[Window Functions: Aggregate, Value, Ranking](#window-functions)</b>
  - <b>[Table JOINs: Left, Right, Inner, Outer, Special](#table-joins)</b>
  - <b>[SQL Clauses: Group, Order, Limit, Offset](#sql-clauses)</b>
---

## Overview of SQL Data Structures

<div>
<table>
	  <tr>
    	  <td style="margin:2px;">
<p align='center'><img src='https://github.com/kariemoorman/didactic-diy/blob/main/tutorials/sql/images/sql_tables-sql_data_structures.drawio.png'  width='80%'/></p>
        </td>
    </tr>
</table>
</div>

---

## DQL 

### Window Functions
---

#### Aggregate Window Functions 

<p align='center'><img src='https://github.com/kariemoorman/didactic-diy/blob/main/tutorials/sql/images/sql_window_functions-aggregate_window.drawio.png' width='95%'/></p>

#### Value Window Functions

<p align='center'><img src='https://github.com/kariemoorman/didactic-diy/blob/main/tutorials/sql/images/sql_window_functions-value_window.drawio.png' width='95%'/></p>

#### Ranking Window Functions

<p align='center'><img src='https://github.com/kariemoorman/didactic-diy/blob/main/tutorials/sql/images/sql_window_functions-rank_window.drawio.png' width='95%'/></p>

---
### Table JOINs
---
<div>
<table>
	  <tr>
    	  <td style="margin:10px;">
        	<p align='center'><img src="https://github.com/kariemoorman/didactic-diy/blob/main/tutorials/sql/images/sql_joins-3-left_joins.drawio.png" width="95%"/></p>
      	</td>
        <td style="margin:10px">
          <p align='center'><img src="https://github.com/kariemoorman/didactic-diy/blob/main/tutorials/sql/images/sql_joins-3-right_joins.drawio.png" width="95%"/></p>
        </td>
    </tr>
</table>

<table>
  <tr>
    <td style="margin:10px;">
	<p align='center'><img src="https://github.com/kariemoorman/didactic-diy/blob/main/tutorials/sql/images/sql_joins-3-full_joins.drawio.png" width="95%"/></p>
    </td>
    <td style="margin:10px">
	<p align='center'><img src="https://github.com/kariemoorman/didactic-diy/blob/main/tutorials/sql/images/sql_joins-3-special_joins.drawio.png" width="95%"/></p>
    </td>
  </tr>
</table>
</div>

---
### SQL Clauses
---

<div>
<p><b>GROUP BY</b>: The GROUP BY clause groups rows based on values of one or more columns:  <code>GROUP BY [column] [ASC | DESC]</code>.</p>
</div>

<div>
<p><b>ORDER BY</b>: The ORDER BY clause sorts results based on values of one or more columns: <code>ORDER BY [column] [ASC | DESC]</code>.</p>
</div>

<div>
<p><b>LIMIT</b>: The LIMIT clause determines the [number] rows returned by the query: <code>LIMIT [number]</code>. </p>
</div>

<div>
<p><b>OFFSET</b>: The OFFSET clause skips [number] rows before returning query results: <code>OFFSET [number]</code>.</p>
</div>

<p><code>SELECT                 
    fruit               
   ,COUNT(*) AS count   
 FROM fruit_table       
   GROUP BY fruit       
   ORDER BY fruit ASC   
   LIMIT 4 OFFSET 1;   </code></p>

---

<p align='center'><b>License: <a href='https://choosealicense.com/licenses/gpl-3.0/'>GNU General 
Public License v3.0</a></b></p>
