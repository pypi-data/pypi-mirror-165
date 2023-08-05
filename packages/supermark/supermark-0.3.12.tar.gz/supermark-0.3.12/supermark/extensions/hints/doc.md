# Hints

Hints are boxes with information that is only visible when the reader clicks on the header.
The top of the hint is specified with a YAML section. 
The content of the hint is provided as post-YAML section, directly following the YAML header.
It ends after two consecutive empty lines.

---
type: hint
title: Hint about Something
---
Within the content you can have lists:

* 10.0.0.0/8
* 172.16.0.0/12
* 192.168.0.0/16

And you can continue.

**Remember:** Hints should be helpful. 


```yaml
---
type: hint
title: Hint about Something
---
Within the content you can have lists:

* 10.0.0.0/8
* 172.16.0.0/12
* 192.168.0.0/16

An you can coninue.

**Remember:** Hints should be helpful. 
```






:hint: This is a hint that is only visible after clicking a button.



:hint: This is another hint that is only visible after clicking a button.