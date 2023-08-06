from .dataset import Dataset
import numpy as np

def sample_by_class(ds: Dataset, nb_samples_per_class, seed=2021):
    #set fixed seed for rng
    rng = np.random.default_rng(seed=seed)

    all_labels = ds.get_labels(fill=True)

    boolean_samples = np.zeros(ds.included_samples.size, dtype=bool)

    #iterate over labels in dataset
    for label_id, label in ds.get_label_table():

        label_bools = all_labels == label_id

        nb_label_samples = label_bools.sum()

        if nb_label_samples > nb_samples_per_class:
            t_mask = np.zeros(nb_label_samples, dtype=bool)
            t_mask[rng.choice(nb_label_samples, nb_samples_per_class, replace=False)] = True
            label_bools[label_bools] = t_mask

        boolean_samples[label_bools] = True

    ds.included_samples = boolean_samples

    return ds

def sample_from_list(dataset_list, nb_samples_per_dataset=None, total_nb_samples=None):
    merged_dataset = None

    number_of_samples = [ds.get_nb_samples() for ds in dataset_list]
    max_nb_samples = sum(number_of_samples)

    if total_nb_samples is None:
        total_nb_samples = max_nb_samples
    if total_nb_samples > max_nb_samples:
        print('WARNING: requested total number of samples ({0}) was greather then sum of all samples in dataset list ({1}).'
              ' \n Returning combination of all dataset.'.format(total_nb_samples, max_nb_samples))

    for ds in dataset_list:
        if nb_samples_per_dataset is None:
            percentage = total_nb_samples/max_nb_samples
            nb_samples_per_dataset = np.floor(dataset.get_nb_samples()*percentage)
        sample_random(ds, nb_samples_per_dataset)
        if merged_dataset is None:
            merged_dataset = ds
        else:
            merged_dataset.add(ds)

    return merged_dataset

def sample_random(dataset, nb_points, seed=2021):
    assert dataset.included_samples.dtype == np.bool

    # set fixed seed for rng
    rng = np.random.default_rng(seed=seed)

    incluced_bool = dataset.included_samples
    nb_included = np.sum(incluced_bool)

    t_mask = np.zeros(nb_included, dtype=bool)
    t_mask[rng.choice(nb_included, nb_points, replace=False)] = True
    incluced_bool[incluced_bool] = t_mask

    dataset.included_samples = incluced_bool

    return dataset
