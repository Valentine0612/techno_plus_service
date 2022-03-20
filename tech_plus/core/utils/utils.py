from ..models import Form_7, Operation


def load_data(val, param, model):
    kwargs = {}
    kwargs[param] = val
    if val:
        data = model.objects.filter(**kwargs)
    else:
        data = model.objects.none()
    return data


def create_table_form8(other_context, **kwargs):
    context = {}
    try:
        context.update(other_context)
    except KeyError:
        pass
    context['metadata'] = 'form_8'
    form_7_queryset = Form_7.objects.filter(form_8=kwargs['pk'])
    form_7 = form_7_queryset.first()
    if form_7:
        context['operations'] = form_7.has_operations.all()
        context['queryset'] = form_7_queryset
        durations = {}
        products = {}
        count_of_work = {}
        count_of_production = {}
        for obj in form_7_queryset:
            for oper in obj.has_operations.all():

                if not oper.name in count_of_work:
                    if oper.duration != 0:
                        count_of_work[oper.name] = [
                            round(float(oper.products*60/oper.duration), 2)]
                    else:
                        count_of_work[oper.name] = [0.0]
                else:
                    if oper.products and oper.duration:
                        count_of_work[oper.name].append(
                            round(float(oper.products*60/oper.duration), 2))
                    else:
                        count_of_work[oper.name].append('-')

                if not oper.name in count_of_production:
                    if oper.products != 0:
                        count_of_production[oper.name] = [
                            round(float(oper.duration/oper.products), 2)]
                    else:
                        count_of_production[oper.name] = [0.0]
                else:
                    if oper.products and oper.duration:
                        count_of_production[oper.name].append(
                            round(float(oper.duration/oper.products), 2))
                    else:
                        count_of_production[oper.name].append('-')
                if not oper.name in durations:
                    durations[oper.name] = oper.duration
                else:
                    durations[oper.name] += oper.duration
                if not oper.name in products:
                    products[oper.name] = oper.products
                else:
                    products[oper.name] += oper.products
        sum_count_of_work = {}
        for key, value in count_of_work.items():
            sum_count_of_work[key] = round(
                sum([float(i) for i in value if type(i) == float or i.isdigit()]), 2)
        sum_count_of_product = {}
        average_count_of_product = {}
        ntz = {}

        for key, value in count_of_production.items():
            summ = sum([float(i)
                       for i in value if type(i) == float or i.isdigit()])
            items = len(value) - value.count('-')
            sum_count_of_product[key] = round(summ, 2)
            average_count_of_product[key] = round(float(summ/items), 4)
            operation = form_7.has_operations.get(name=key)
            ntz[key] = round(round((round(float(summ/items), 4)*100), 4) /
                             (60*(100-(operation.ratio.npzr+operation.ratio.no+operation.ntp.ntp))), 4)
        context['count_of_work'] = count_of_work
        context['count_of_product'] = count_of_production
        context['sum_count_of_work'] = sum_count_of_work
        context['sum_count_of_product'] = sum_count_of_product
        context['ntz'] = ntz
        context['average_count_of_product'] = average_count_of_product
        context['durations'] = durations
        context['products'] = products
    return context


def get_form_1_data(other_context, **kwargs):
    context = {}
    try:
        context.update(other_context)
    except KeyError:
        pass
    form_7_queryset = Form_7.objects.filter(form_8=kwargs['pk'])
    form_7 = form_7_queryset.first()
    if form_7:
        context['operations'] = form_7.has_operations.all()
        context['queryset'] = form_7_queryset
        products = {}
        sum_products = {}
        for obj in form_7_queryset:
            for oper in obj.has_operations.all():
                if oper.products != 0:
                    if oper.name in products.keys():
                        products[oper.name] += f"+{str(oper.products)}"
                        sum_products[oper.name] += oper.products
                    else:
                        products[oper.name] = f"={str(oper.products)}"
                        sum_products[oper.name] = oper.products
        
        context['products'] = products
        context['sum_products'] = sum_products
    return context


def get_form_2_data(other_context, **kwargs):
    context = {}
    try:
        context.update(other_context)
    except KeyError:
        pass
    ntz = create_table_form8(other_context=other_context, pk=kwargs['pk'])['ntz']
    form_1 = get_form_1_data(other_context=other_context, pk=kwargs['pk'])
    context['ntz'] = ntz
    context['sum_products'] = form_1['sum_products']
    total_ntz = {}
    for key in ntz.keys():
        total_ntz[key] = round(ntz[key]*float(form_1['sum_products'][key]),4)
    context['total_ntz'] = total_ntz
    context['operations'] = form_1['operations']
    return context


def get_form_3_data(other_context, **kwargs):
    context = {}
    try:
        context.update(other_context)
    except KeyError:
        pass
    form_2_data = get_form_2_data(other_context=other_context, pk=kwargs['pk'])
    operations = form_2_data['operations']
    total_ntz = form_2_data['total_ntz']
    workmans = {}
    for operation in operations:
        if operation.member_operation.all():
            for member in operation.member_operation.all():
                if member.workman in workmans:   
                    workmans[member.workman] += total_ntz[str(member.operation)]
                else:
                    workmans[member.workman] = total_ntz[str(member.operation)]
    measure_workmans = {}
    average_rank = 0
    process_measure = context['object'].process_meter
    try:
        main_measure = int(context['object'].main_measure.code.split(' ')[0])
    except:
        main_measure = 1
    for key, value in workmans.items():
        digit = round(value*main_measure/float(process_measure),2)
        measure_workmans[key] = digit
        try:
            rank = int(key.name.split(' ')[1])
        except:
            rank = None
        if rank:
            average_rank += digit*rank
    context['measure_workmans'] = measure_workmans
    context['workmans'] = workmans
    sum_workmans = sum(workmans.values())
    sum_measure_workmans = sum(measure_workmans.values())
    context['sum_workmans'] = round(sum_workmans,2)
    context['sum_measure_workmans'] = round(sum_measure_workmans,2)
    context['k_sum_workmans'] = round(sum_workmans*float(context['object'].workman_k),2)
    context['k_sum_measure_workmans'] = round(sum_measure_workmans*float(context['object'].workman_k),2)
    try:
        context['average_rank'] = round(average_rank/sum_measure_workmans,1)
    except:
        context['average_rank'] = 0
    return context


def get_form_4_data(other_context, **kwargs):
    context = {}
    try:
        context.update(other_context)
    except KeyError:
        pass
    form_2_data = get_form_2_data(other_context=other_context, pk=kwargs['pk'])
    operations = form_2_data['operations']
    total_ntz = form_2_data['total_ntz']
    machines = {}
    is_driver = {}
    for operation in operations:
        if operation.machine_operation.all():
            for machine in operation.machine_operation.all():

                if machine.machine in machines:   
                    machines[machine.machine] += total_ntz[str(machine.operation)]
                else:
                    machines[machine.machine] = total_ntz[str(machine.operation)]
                if  machine.is_driver:
                    is_driver[machine.machine] = True
                else:    
                    is_driver[machine.machine] = False
    measure_machines = {}
    process_measure = context['object'].process_meter
    try:
        main_measure = int(context['object'].main_measure.code.split(' ')[0])
    except:
        main_measure = 1
    sum_of_driver = 0
    for key, value in machines.items():
        digit = round(value*main_measure/float(process_measure),2)
        measure_machines[key] = digit
        if is_driver[key]:
            sum_of_driver += digit

    context['machines'] = machines
    context['is_driver'] = is_driver
    context['measure_machines'] = measure_machines
    context['sum_of_driver'] = sum_of_driver
    
    return context

def get_form_5_data(other_context, **kwargs):
    context = {}
    try:
        context.update(other_context)
    except KeyError:
        pass
    form_2_data = get_form_2_data(other_context=other_context, pk=kwargs['pk'])
    operations = form_2_data['operations']
    measure = {}
    materials = {}
    code = {}
    process_measure = context['object'].process_meter
    try:
        main_measure = int(context['object'].main_measure.code.split(' ')[0])
    except:
        main_measure = 1
    for operation in operations:
        if operation.material_operation.all():
            for material in operation.material_operation.all():
                if material.material in materials:   
                    materials[material.material] += float(material.count)
                else:
                    materials[material.material] = float(material.count)
                measure[material.material] = material.material.measurement
                code[material.material] = material.material.title
    material_measure = {}
    for key, value in materials.items():
        material_measure[key] = round(value*main_measure/float(process_measure),2)
    context['materials'] = materials
    context['measure'] = measure
    context['code'] = code
    context['material_measure'] = material_measure
     
    return context


def get_form_6_data(other_context, **kwargs):
    context = {}
    try:
        context.update(other_context)
    except KeyError:
        pass
    form_2_data = get_form_2_data(other_context=other_context, pk=kwargs['pk'])
    form_3_data = get_form_3_data(other_context=other_context, pk=kwargs['pk'])
    form_4_data = get_form_4_data(other_context=other_context, pk=kwargs['pk'])
    form_5_data = get_form_5_data(other_context=other_context, pk=kwargs['pk'])
    context['operations'] = form_2_data['operations']
    context['k_sum_measure_workmans'] = form_3_data['k_sum_measure_workmans']
    context['average_rank'] = form_3_data['average_rank']
    context['sum_of_driver'] = form_4_data['sum_of_driver']
    context['measure_machines'] = form_4_data['measure_machines']
    context['material_measure'] = form_5_data['material_measure']
    return context