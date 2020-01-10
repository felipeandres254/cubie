<?php

namespace App\Hardware\Modules;

use \App\Hardware\Exceptions\GPIOException;

define('GPIO_DIRECTORY', '/sys/class/gpio');

class GPIO
{
    /**
     * The GPIO pin
     *
     * @var string
     */
    private $pin;
    public function getPin () { return $this->pin; }

    /**
     * The GPIO pin address
     *
     * @var int
     */
    private $address;
    public function getAddress () { return $this->address; }

    /**
     * The GPIO pin direction
     *
     * @var string
     */
    private $direction;
    public function getDirection () { return $this->direction; }

    /**
     * The GPIO pin value
     *
     * @var bool
     */
    public function getValue () {
        $value = file_get_contents(GPIO_DIRECTORY . '/gpio' . $this->address . '/value');
        return trim($value) == '1';
    }
    public function setValue ($nValue) {
        if ($this->direction != 'out') return;
        $nValue = ((bool)$nValue) ? '1' : '0';
        file_put_contents(GPIO_DIRECTORY . '/gpio' . $this->address . '/value', $nValue);
    }

    /**
     * Instantiate a GPIO pin
     *
     * @param  string  $pin
     * @param  string  $direction
     */
    function __construct ($pin, $direction = 'in') {
        try {
            $this->pin = strtolower($pin);

            $regex = '/p(?P<port>[a-z])(?P<number>[0-9]*)/';
            preg_match_all($regex, $this->pin, $matches, PREG_SET_ORDER, 0);
            $port = $matches[0]['port'];
            $number = (int)$matches[0]['number'];

            $this->address = 32*(ord($port) - 97) + $number;
        } catch (Exception $e) {
            throw new GPIOException('Invalid pin format!');
        }

        if ($direction != 'in' && $direction != 'out') {
            throw new GPIOException('Invalid pin direction!');
        }
        $this->direction = $direction;

        // Open the GPIO pin
        if (file_exists(GPIO_DIRECTORY . '/gpio' . $this->address)) {
            file_put_contents(GPIO_DIRECTORY . '/unexport', $this->address);
        }
        file_put_contents(GPIO_DIRECTORY . '/export', $this->address);
        file_put_contents(GPIO_DIRECTORY . '/gpio' . $this->address . '/direction', $this->direction);
        $this->setValue(0);
    }

    /**
     * Remove reference to this GPIO pin
     */
    function __destruct () {
        $this->setValue(0);
        file_put_contents(GPIO_DIRECTORY . '/unexport', $this->address);
    }
}
