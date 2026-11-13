# CITE AI for Cyber Security — workshop package

**Attendees start here: [Participant workbook](participant/teaching/PARTICIPANT-WORKBOOK.html).** It links the complete print/offline no-account packet. Handouts also have editable Markdown sources. The participant ZIP contains only attendee instructions, answer material, setup/source references and safe lab assets; internal proposals/reviews remain in the team source folders.

**Facilitators:** use the [facilitator guide](FACILITATOR-GUIDE.html) for timings, debriefs and full prompts, plus [computed agenda](participant/teaching/AGENDA.html), [source mapping](SOURCES-AND-MAPPING.html) and [verification report](VERIFICATION.md). Facilitator source-audit records are in `facilitator/`, outside the participant ZIP.

`CITE-AI-Cybersecurity-Workshop.pptx` is editable, with 21 timed core slides and four hidden support views. Use the Help buttons during work and Return to lab on support views. The hidden views add zero minutes. Scope: fictional policy checklist, deterministic synthetic log triage, static local HTML report. Default live route is approved Claude; local Python and paper review need no AI account. Paper work is recorded as review, not execution.

## Prepare the disposable lab

Installation/authentication are prework. Use an organization-approved disposable environment; a new folder is not isolation. Python 3.11+ is the participant floor; Linux rehearsal target is Ubuntu 24.04/Python 3.12. Actual reference execution here used macOS/Python 3.14.9. Linux/WSL runtime rehearsal remains NOT RUN.

Inside that prepared environment, place this package's `participant/teaching` and `participant/linux` folders under `~/cite-workshop/` as siblings. Open a terminal in `~/cite-workshop/teaching`, inspect the workbook R0 commands, then create a fresh `work/` folder. Do not run from the repository root. Use fresh output names on reruns; reference scripts refuse to overwrite output. No GitHub account, SSH key, pip, Node, plugin, scanner or server is needed. A print-only attendee needs only the complete no-account packet.

## Delivery and limitations

Native PowerPoint PDF export: **NOT RUN — awaiting user approval**. The export approval request was canceled without authorization. It was not retried. No exported PDF, PDF raster or native visual-review claim is supplied. The one-slide probe PPTX is a tooling artifact, not part of the session. Handout HTML has local print CSS; no external assets, scripts or invented public URLs. These HTML handouts are not slide renders.

Coordinator-relayed final specialist findings have been resolved and regression-checked; see the verification report. Structural and reference-code checks do not establish classroom pacing, agent inference, participant-generated correctness, browser rendering or Linux/WSL installation success.

## Reproduce in this repository

Use the coordinator-prepared document interpreter recorded in `../integration/BUILD-APPROACH.md`. Run `prepare_manifest.py`, `build_deck.py`, `package_workshop.py`, then `verify_final.py` from `Workshop-Team/integration/` via that interpreter (the scripts resolve paths themselves). Source/build files live there; source design tokens are under `Workshop-Team/design/`, source teaching assets under `Workshop-Team/teaching/`, and read-only brand assets under root `Files/`. No original builder is imported or executed. No dependencies are installed and no native-export script is invoked by this build sequence.
