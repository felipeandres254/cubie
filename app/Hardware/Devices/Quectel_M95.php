<?php

namespace App\Hardware\Devices;

use Illuminate\Support\Facades\Log;
use \App\Hardware\Modules\GPIO;

class Quectel_M95
{
    /**
     * The module POWER pin
     *
     * @var  \App\Hardware\Modules\GPIO
     */
    private $POWER;

    /**
     * The module STATUS pin
     *
     * @var  \App\Hardware\Modules\GPIO
     */
    private $STATUS;

    /**
     * Instatiate the module
     */
    function __construct () {
        $this->POWER = new GPIO('PG1', 'out');
        $this->STATUS = new GPIO('PI3');
        $this->POWER->setValue(0);
    }

    /**
     * Turn on the module
     *
     * @param  bool  $logging
     */
    public function power_on ($logging = false) {
        if ($logging) {
            Log::channel('quectel-m95')->info('Turning on...');
        }
        while (!$this->STATUS->getValue()) {
            $this->POWER->setValue(1);
        }
        $this->POWER->setValue(0);
        sleep(1);
        if ($logging) {
            Log::channel('quectel-m95')->info('Module turned on!');
        }
    }

    /**
     * Turn off the module
     *
     * @param  bool  $logging
     */
    public function power_off ($logging = false) {
        if ($logging) {
            Log::channel('quectel-m95')->info('Turning off...');
        }
        while ($this->STATUS->getValue()) {
            $this->POWER->setValue(1);
        }
        $this->POWER->setValue(0);
        sleep(1);
        if ($logging) {
            Log::channel('quectel-m95')->info('Module turned off!');
        }
    }

    /**
     * Reset the module
     *
     * @param  bool  $logging
     */
    public function reset ($logging = false) {
        if ($logging) {
            Log::channel('quectel-m95')->info('Restarting module...');
        }
        $this->power_off();
        $this->power_on();
        if ($logging) {
            Log::channel('quectel-m95')->info('Module ready!');
        }
    }
}
