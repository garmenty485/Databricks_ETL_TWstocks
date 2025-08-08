---
marp: true
theme: default
header: '![class:databricks-emblem](Databricks-Emblem.png)'
style: |
  header {
    position: absolute;
    top: 20px;
    right: 32px;
    width: 200px;
    height: auto;
    background: none;
    box-shadow: none;
    z-index: 10;
  }
  header img {
    width: 200px;
    height: auto;
    margin: 0;
    box-shadow: none;
    background: none;
  }
---
<style>
h1 {
  font-size: 2.5em;
}
h2 {
  font-size: 1.8em;
}
li, ul, p {
  font-size: 1.3em;
}
.name {
  margin-top: 60px;
  font-size: 0.9em;
}
</style>

# Databricks_ETL_TWstocks

<div class="name">
Chia-Ming Hu (Ken)
</div>
<div class="name">
Github repo : https://github.com/garmenty485/Databricks_ETL_TWstocks
</div>

---

# Content

- Run through the process  
- Main obstacles during development

---

![class:databricks-emblem](medallion.JPG)

---

# 1. Run through the process

 - Setup the Lakeflow Declarative Pipeline (DLT)
 - First batch  
 - Following batches 

---
# 2. Obstacles during development

 - How Autoloader handles schema changes
 - Notebooks main language  
 - DLT distributed computation (shuffling) 
