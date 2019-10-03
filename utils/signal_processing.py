def mvg_avg(new_x, last_x, discount_factor):
    return (1.0 - discount_factor) * new_x + discount_factor * last_x