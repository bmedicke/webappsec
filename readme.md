# Web Application Security

> Exploits are the closest thing to “magic spells”
> we experience in the real world:<br>
> Construct the right incantation,
> gain remote control over device.
>
> @halvarflake

---


<!-- vim-markdown-toc GFM -->

* [Task 1, Hacking](#task-1-hacking)
* [Task 2, Secure Coding](#task-2-secure-coding)
* [Task 3, Secure Coding 2](#task-3-secure-coding-2)
	* [Template, Vulnerability Remediation](#template-vulnerability-remediation)

<!-- vim-markdown-toc -->

## Task 1, Hacking

[**Testing Pen-Test Sites**, 2-3h](task1.md)

* create an account or download a VM
* do excercises for 1-2 hours
* write a small report (2-3 pages)
* how was the setup?
* how was the usability?
* what did you learn/what VMs did you try?
* submit until Monday, November 23rd 2020

## Task 2, Secure Coding

[**How's your framework doing?**, 2-3h](task2.md)

* Features:
	* create a todo
	* list all todos
	* show a single todo
	* delete a single todo
* initially: single-user, in-memory
* later: multi-user, SQL-Database (still in memory)
* bonus: OAuth2, XML/XEE?
* review and test with netsparker
* [basic steps](https://andreashappe.github.io/lecture-web-security/presentation-web-app-sec/presentation.html#/basic-steps)

## Task 3, Secure Coding 2

[**Describe Vulnerability Remediation**, 1-2PT](task3.md)

* Beschreibung von zwei Gegenmassnahmen
* Vorschlag im OWASP Juice Shop
* Alternativ auch andere Software-Projekte
* Zwischenabgabe:
* check ob Umfang passt (1-3 Gegenmassnahmen)
* [hints for juiceshop](https://andreashappe.github.io/lecture-web-security/presentation-web-app-sec/presentation.html#/hints-for-juiceshop)
* [Alternativen fuer 1-2 Gegenmassnahmen](https://andreashappe.github.io/lecture-web-security/presentation-web-app-sec/presentation.html#/alternativen-f%C3%BCr-1-2-gegenmassnahmen)

### Template, Vulnerability Remediation

```md
# challenge: Name of Challenge

2-3 sentences describing the challenge

## The Vulnerability

What is the vulnerability?

## Where to find in the Code?

File:line

# Fixing the Vulnerability

## Potential fixes

Describe how this could be fixed, i.e., if different solutions exist, how to chose a potential fix

## The chosen Fix

Show in the source code how this was fixed.

## How to verify that the fix worked?

Example how do test for the vulnerability and check that it is not there anymore.

## How to spot vulnerabilities like this?

grep-patterns, how to find similar vulnerabilities?

# Related Work/Links

- links to web-pages, articles, etc. that you used while writing this
```
