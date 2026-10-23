# Scoping Decision Trees (v3.3 / Danzell)

## Whole organisation vs sub-set
Default and strongly preferred: whole organisation. A sub-set is acceptable when segregated by firewall or VLAN, but under Danzell every exclusion must be JUSTIFIED, out-of-scope areas described to the assessor (not published), and all in-scope legal entities named (name, address, registration number). A scope that excludes end-user devices is not acceptable. Whole-organisation scope is required for the bundled insurance. Individual per-entity certificates are available for a small additional charge.

## Cloud services — always in
If organisational data or services live in a cloud service, that service is IN SCOPE and cannot be excluded (Danzell adds a formal definition of "cloud service" and makes this definitive). Apply the shared-responsibility model:
- IaaS: customer owns most themes (configuration, updates, access, malware on their instances); provider owns physical/hypervisor.
- PaaS: split — customer owns access control, configuration of the platform surface.
- SaaS: provider owns most technical controls; customer ALWAYS owns user access control and MFA enablement.
Where the provider implements a control, you must confirm it is contractually committed (terms/trust documentation). MFA on every cloud service is the customer's responsibility regardless of model.

## BYOD decision tree
1. Device accesses organisational data or services (email, files, SaaS)? → IN SCOPE.
2. Used ONLY for native voice calls, native SMS, or as an MFA authenticator app? → OUT.
3. Whose device? Employee/volunteer/trustee/university-researcher BYOD → IN. Students, third-party contractors, MSP administrators' own devices, customers → OUT (but organisation-owned ACCOUNTS those parties use remain in scope).

## Home and remote working
- All home/remote working devices (corporate or BYOD) are in scope — "home and remote working" wording since Willow covers cafés, trains, anywhere.
- Home ISP/user-owned routers: OUT of scope; the device's software firewall becomes the enforced boundary control.
- Organisation-supplied home routers: IN scope (full firewall controls).
- Corporate VPN in use: the internet boundary shifts to the corporate, virtual or cloud firewall — that firewall carries the firewall controls.

## Wireless and other edges
Wireless devices: in scope if attackable via the internet; out if only attackable within signal range or part of the home ISP router. "Point in time": compliance is asserted as at the certificate ISSUE DATE — but the Danzell board declaration commits the organisation to maintaining compliance throughout the certification period, so treat drift as a declaration problem, not a technicality.

## Common scoping mistakes to flag
Excluding "just the dev network" without VLAN/firewall segregation; forgetting SaaS admin consoles; treating MSP-operated accounts as out of scope; leaving legacy unsupported servers "in scope but accepted" (fail — remove or air-gap the sub-set from the internet); claiming BYOD out of scope while staff read email on personal phones; scoping out cloud services (impossible under Danzell).
