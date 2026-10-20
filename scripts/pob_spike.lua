-- One-shot experiment adapter, not the production worker protocol (EXAI-003).
local json = require("dkjson")
local request = assert(json.decode(io.read("*a")))
local started = os.clock()
dofile("HeadlessWrapper.lua")
assert(__mainObject__ and not __mainObject__.promptMsg and build, "startup_failed")
local startup = os.clock() - started

local function recalculate()
	build.buildFlag = true
	runCallback("OnFrame")
	assert(not __mainObject__.promptMsg, "engine_error")
	build.calcsTab:BuildOutput()
end

if request.operation == "create_fixture" then
	newBuild()
	for id, class in pairs(build.spec.tree.classes) do
		if class.name == "Sorceress" then build.spec:SelectClass(id) end
	end
	build.characterLevel = 90
	build.characterLevelAutoMode = false
	build.skillsTab:PasteSocketGroup("Spark 1/0  1")
	build.mainSocketGroup = 1
	recalculate()
	local nodes = {}
	for id, node in pairs(build.spec.nodes) do
		if not node.alloc and node.type == "Normal" and not node.isAttribute and not node.ascendancyName and node.path and #node.path == 1 then
			nodes[#nodes + 1] = { id = id, name = node.name }
		end
	end
	table.sort(nodes, function(a, b) return a.id < b.id end)
	assert(#nodes >= 2, "fixture_needs_two_start_neighbors")
	build.spec:AllocNode(build.spec.nodes[nodes[1].id])
	recalculate()
	print("EXILEAI_RESULT=" .. json.encode({xml = build:SaveDB("code"), neighbors = nodes, class = build.spec.curClassName, skill = "Spark", points = {build.spec:CountAllocNodes()}}))
	return
end

local function snapshot(metricNames)
	local metrics = {}
	local metricStates = setmetatable({}, {__jsontype = "object"})
	for _, key in ipairs(metricNames) do
		local value = build.calcsTab.mainOutput[key]
		if key == "ChaosMaximumHitTaken" and value == math.huge and build.calcsTab.mainOutput.ChaosInoculation == true then
			metrics[key] = json.null
			metricStates[key] = {state = "immune", reason = "ChaosInoculation"}
		else
			assert(type(value) == "number" and value == value and value > -math.huge and value < math.huge, "missing_or_nonfinite_metric:" .. key)
			metrics[key] = value
		end
	end
	local allocated = {}
	local notDirectlyConnected = {}
	for id, node in pairs(build.spec.allocNodes) do
		if node.type ~= "ClassStart" and node.type ~= "AscendClassStart" and not node.connectedToStart then
			assert(request.operation == "inspect_import", "disconnected_allocation:" .. id)
			notDirectlyConnected[#notDirectlyConnected + 1] = id
		end
		allocated[#allocated + 1] = id
	end
	table.sort(allocated)
	table.sort(notDirectlyConnected)
	local requirements = {}
	for _, attr in ipairs({"Str", "Dex", "Int"}) do
		local available = build.calcsTab.mainOutput[attr] or 0
		local required = build.calcsTab.mainOutput["Req" .. attr] or 0
		requirements[attr] = {available = available, required = required, deficit = math.max(0, required - available)}
	end
	return {metrics = metrics, metric_states = metricStates, points = {build.spec:CountAllocNodes()}, allocated = allocated, not_directly_connected = notDirectlyConnected, requirements = requirements}
end

newBuild()
local defaultPlaceholders = copyTable(build.configTab.configSets[build.configTab.activeConfigSetId].placeholder)
local loadStart = os.clock()
loadBuildFromXML(assert(request.xml), "ExileAI integration fixture")
assert(not __mainObject__.promptMsg and build.spec and build.calcsTab, "import_failed")
assert(build.spec.treeVersion == request.tree_version, "unsupported_tree_version")
recalculate()
local imported = snapshot(request.metrics)
local loadTime = os.clock() - loadStart
if request.operation == "inspect_import" then
	local expected = {}
	local actual = {}
	local added = {}
	local missing = {}
	for _, id in ipairs(request.expected_nodes) do expected[id] = true end
	for _, id in ipairs(imported.allocated) do
		actual[id] = true
		if not expected[id] then
			local node = build.spec.allocNodes[id]
			added[#added + 1] = {id = id, name = node.name, type = node.type, free = node.isFreeAllocate == true, granted = node.isGrantedPassive == true}
		end
	end
	for _, id in ipairs(request.expected_nodes) do
		if not actual[id] then missing[#missing + 1] = id end
	end
	print("EXILEAI_RESULT=" .. json.encode({
		imported = imported, class = build.spec.curClassName,
		allocation_reconciliation = {added = added, missing = missing, exact_match = #added == 0 and #missing == 0},
		tree_version = build.spec.treeVersion, main_socket_group = build.mainSocketGroup,
		config_inputs = build.configTab.input, original_xml = request.xml,
		benchmark_eligible = false, assumption_policy = "as-imported-unverified",
		timing_cpu_seconds = {startup = startup, load = loadTime}
	}))
	return
end
assert(#imported.allocated == #request.expected_nodes, "import_changed_allocation")
for i, id in ipairs(request.expected_nodes) do assert(imported.allocated[i] == id, "import_changed_allocation") end

if request.operation == "benchmark_swap" then
	loadBuildFromXML(assert(request.benchmark_xml), "ExileAI conservative boss benchmark")
	assert(not __mainObject__.promptMsg, "benchmark_import_failed")
	recalculate()
	local normalized = snapshot(request.metrics)
	assert(#normalized.allocated == #imported.allocated, "normalization_changed_allocation")
	for i, id in ipairs(imported.allocated) do assert(normalized.allocated[i] == id, "normalization_changed_allocation") end
end

-- The spike supports one explicit scenario input; objective selection stays outside PoB.
assert(request.scenario.id == "solo-sustained-pinnacle-v1", "unsupported_scenario")
local input = build.configTab.input
-- Preserve quest rewards, resistance penalties, and upstream defaults. Preflight
-- rejects imported conditional overrides until a complete auditor exists.
local placeholders = build.configTab.configSets[build.configTab.activeConfigSetId].placeholder
for key in pairs(placeholders) do placeholders[key] = nil end
for key, value in pairs(defaultPlaceholders) do placeholders[key] = value end
for key, value in pairs(request.scenario.config) do input[key] = value end
build.configTab:BuildModList()
recalculate()
local before = snapshot(request.metrics)
local effectiveConfig = copyTable(build.configTab.input)
for _, attr in ipairs({"Str", "Dex", "Int"}) do
	assert(before.requirements[attr].deficit == 0, "baseline_attribute_requirement_failed:" .. attr)
end
local frozenModes = {}
for id, node in pairs(build.spec.allocNodes) do frozenModes[id] = node.allocMode or 0 end
local beforeXML = build:SaveDB("code")
local spec = build.spec
local remove = spec.nodes[request.action.remove]
local add = spec.nodes[request.action.add]
assert(remove and add and remove ~= add, "invalid_node_ids")
local function ordinary(node)
	return node.type == "Normal" and not node.isAttribute and not node.ascendancyName and not node.isFreeAllocate and (node.allocMode or 0) == 0
end
assert(ordinary(remove) and ordinary(add), "unsupported_node_type")
assert(remove.alloc and not add.alloc, "invalid_allocation_state")
assert(#remove.depends == 1, "removal_is_not_a_leaf")
local calcStart = os.clock()
local previousAllocMode = spec.allocMode
spec.allocMode = 0
spec:DeallocNode(remove)
assert(add.path and #add.path == 1, "addition_requires_more_than_one_point")
assert(not add.pathRoot or (add.pathRoot.allocMode or 0) == 0, "addition_promotes_weapon_branch")
spec:AllocNode(add)
spec.allocMode = previousAllocMode
recalculate()
local after = snapshot(request.metrics)
for _, attr in ipairs({"Str", "Dex", "Int"}) do
	assert(after.requirements[attr].deficit == 0, "attribute_requirement_failed:" .. attr)
end
for i, count in ipairs(before.points) do assert(after.points[i] == count, "point_budget_changed:" .. i .. ":" .. count .. ":" .. after.points[i]) end
assert(#before.allocated == #after.allocated and not remove.alloc and add.alloc, "unexpected_allocation_change")
for id, mode in pairs(frozenModes) do
	if id ~= request.action.remove then
		local node = build.spec.allocNodes[id]
		assert(node and (node.allocMode or 0) == mode, "fixed_allocation_changed:" .. id)
	end
end
assert(build.spec.curClassName and build.mainSocketGroup, "build_context_lost")
local deltas = {}
local deltaStates = setmetatable({}, {__jsontype = "object"})
for key, value in pairs(after.metrics) do
	if type(value) == "number" and type(before.metrics[key]) == "number" then
		deltas[key] = value - before.metrics[key]
	else
		deltas[key] = json.null
		deltaStates[key] = {state = "not_numeric", before = before.metric_states[key] or {state = "finite"}, after = after.metric_states[key] or {state = "finite"}}
	end
end
print("EXILEAI_RESULT=" .. json.encode({
	imported = imported, before = before, after = after, deltas = deltas, delta_states = deltaStates,
	scenario = request.scenario, action = request.action,
	assumption_audit = request.assumption_audit,
	resolved_config_inputs = effectiveConfig,
	original_xml = request.xml, audited_xml = beforeXML, modified_xml = build:SaveDB("code"),
	tree_version = spec.treeVersion, class = spec.curClassName,
	timing_cpu_seconds = {startup = startup, load = loadTime, mutation_recalculation = os.clock() - calcStart}
}))
