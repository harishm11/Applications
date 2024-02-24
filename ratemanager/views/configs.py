'''
This file stores the app configs for ratemanager, stuff like No of Ratevars, and some temporary stuff that are needed for the ETL process like maps for cov short code to Coverage Name.
'''

cov_mapping = {
        'UMPD': 'UninsuredMotoristPD',
        'BI': 'BodilyInjury',
        'PD': 'PropertyDamage',
        'UM': 'UninsuredMotoristBI',
        'MED': 'Medical',
        'COMP': 'Comprehensive',
        'COLL': 'Collission',
        'ADD EQUI': 'AdditionaEquipment',
        'RENTAL RE': 'RentalReembursement',
        'LOSS OF USE': 'LossOfUse',
        'TOWING': 'Towing',
        'TOW': 'Towing',
        'ALL OTHER COVERAGES': 'Other',
        'RENT': 'RentalReembursement',
        'All': 'All'
    }

ratevars = [
        'TermLength',
        'UMPDOption',
        'DPS',
        'Symbol',
        'ModelYear ',
        'HighPerfInd ',
        'VehHistInd ',
        'PassiveResType',
        'AntiLockInd ',
        'AntitheftInd',
        'AltFuelInd ',
        'EscInd ',
        'DriverClass',
        'YearsDrivingExperience',
        'StudentAwayInd',
        'VehUseCode',
        'HouseholdComposition',
        'FrequencyBand',
        'SeverityBand',
        'MultiPolicy',
        'GoodDriverDiscInd',
        'PermissiveUserOption',
        'VehicleAge1',
        'RideShareInd',
        'Deductible1',
        'Deductible2',
        'DriverClassCode',
        'VehicleAge2',
        'Limit1',
        'Limit2',
        'Mileage1',
        'Mileage2']


export_details = [
    'Carrier',
    'State',
    'Line of Business',
    'Policy Type',
    'Policy Sub Type',
    'Product Code',
    'UW Company',
    'New Business Effective Date',
    'Renewal Effective Date',
    'Activation Date',
    'Activation Time',
    'Migration Date',
    'Migration Time',
    'Ratebook ID',
    'Ratebook Version'
]

NO_OF_RATING_VARIABLES = 8


ENVIRONMENT_HIERARCHY = {
                        'Draft': 0,
                        'Review': 1,
                        'Final/Approved': 2,
                        'Ready for Upload': 3,
                        'Development': 4,
                        'Integration': 5,
                        'UAT': 6,
                        'Regression': 7,
                        'Pre-Production': 8,
                        'Production Like': 9,
                        'Production': 10
                        }
