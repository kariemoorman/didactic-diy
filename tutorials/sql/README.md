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

### Aggregate Window Functions 

<ul>
<li>
<p><b>AVG</b>: The AVG() function returns the average of a set: <code>AVG(ALL | DISTINCT)</code>. </p>
</li>
<li>
<p><b>MIN</b>: The MIN() function returns the minimum value of a set: <code>MIN(column | expression)</code>.</p>
</li>
<li>
<p><b>MAX</b>: The MAX() function returns the maximum value of a set: <code>MAX(column | expression)</code>.</p>
</li>
<li>
<p><b>COUNT</b>: The COUNT() function returns the number of items in a set: <code>COUNT ([ALL | DISTINCT] column | expression | *)</code>.</p>
</li>
<li>
<p><b>SUM</b>: The SUM() function returns the sum of all values: <code>SUM([ALL | DISTINCT] column)</code>.</p>
</li>
</ul>


### Value Window Functions

<ul>
<li>
<p><b>FIRST_VALUE</b>: The FIRST_VALUE() window function returns the first value in an ordered set of values:</p>  
	<code>FIRST_VALUE(column | expression) OVER (
    PARTITION BY [column]
    ORDER BY [column] [ASC | DESC]
    frame_clause)</code>. 
</li>
<li>
<p><b>LAST_VALUE</b>: The LAST_VALUE() window function returns the last value in an ordered set of values:</p>
	<code>LAST_VALUE(column | expression) OVER (
    PARTITION BY [column]
    ORDER BY [column] [ASC | DESC]
    frame_clause)</code>. 
</li>
<li>
<p><b>LAG</b>: The LAG() window function provides access to a row at a specified physical offset that precedes the current row:</p>
	<code>LAG([column] [, offset_value , default_value ]) OVER (
    PARTITION BY [column]
    ORDER BY [column] [ASC | DESC])</code>. 
</li>
<li>
<p><b>LEAD</b>: The LEAD() window function provides access to a row at a specified physical offset that follows the current row:</p>
	<code>LEAD([column] [, offset_value , default_value ]) OVER (
    PARTITION BY [column]
    ORDER BY [column] [ASC | DESC])</code>. 
</li>
</ul>

### Ranking Window Functions

<ul>
<li>
<p><b>ROW_NUMBER</b>: The ROW_NUMBER()  window function assigns a sequential integer number to each row in the query’s result set:</p>
	<code>ROW_NUMBER() OVER (
    PARTITION BY [column]
    ORDER BY [column] [ASC | DESC])</code>. 
</li>
<li>
<p><b>RANK</b>: The RANK() window function assigns a rank to each row in the partition of a result set. The rank of a row is determined by one plus the number of ranks that come before it. RANK() does not always generate consecutive rank values:</p>
	<code>RANK() OVER (
    PARTITION BY [column]
    ORDER BY [column] [ASC | DESC])</code>. 
</li>
<li>
<p><b>DENSE_RANK</b>: The DENSE_RANK() window function assigns ranks to rows in partitions with no gaps in the ranking values. DENSE_RANK() always generates consecutive rank values:</p>
	<code>DENSE_RANK() OVER (
    PARTITION BY [column]
    ORDER BY [column] [ASC | DESC])</code>. 
</li>
<li>
<p><b>PERCENT_RANK</b>: The PERCENT_RANK() window function calculates the percentile ranking of rows in a result set:</p>
	<code>ROUND(PERCENT_RANK() OVER (
    PARTITION BY [column]
    ORDER BY [column] [ASC | DESC]), [integer])</code>.
</li>
</ul>

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
